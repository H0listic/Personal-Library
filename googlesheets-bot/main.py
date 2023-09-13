import discord
from discord.ext import commands
import gecko_terminal as gt
import formatting as fm
import google_sheets as gs
import config
import asyncio

# Discord bot
bot_prefix = "."
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)
bot.remove_command("help")  # Remove the default help command

# Define rate limit constants
REQUESTS_PER_SECOND = 50
BUCKET_CAPACITY = REQUESTS_PER_SECOND  # Initial capacity equals the rate limit
REFILL_RATE = REQUESTS_PER_SECOND  # Refill the bucket at the same rate as the rate limit

# Initialize the token bucket
token_bucket = BUCKET_CAPACITY


# Function to check and consume tokens from the bucket
async def consume_token():
    global token_bucket
    while True:
        if token_bucket >= 1:
            token_bucket -= 1
            await asyncio.sleep(1 / REQUESTS_PER_SECOND)
        else:
            await asyncio.sleep(0.1)  # Wait a bit before checking again


async def extract_data_fields(extracted_data):
    symbol = extracted_data.get("symbol")
    base_token_price_usd = extracted_data.get("base_token_price_usd")
    reserve_in_usd = extracted_data.get("reserve_in_usd")
    fdv_usd = extracted_data.get("fdv_usd")
    contract = extracted_data.get("contract")
    date = extracted_data.get("timestamp")
    pool_address = extracted_data.get("pool_address")

    return symbol, base_token_price_usd, reserve_in_usd, fdv_usd, contract, date, pool_address


@bot.command()
async def help(ctx, command_name: str = None):
    """Displays information about available commands."""
    if not command_name:
        # Display a list of all available commands
        command_list = [command for command in bot.commands if not command.hidden]
        command_list.sort(key=lambda x: x.name)
        command_names = [cmd.name for cmd in command_list]
        await ctx.send(f"Available commands: {', '.join(command_names)}")
    else:
        # Display information about a specific command
        command = bot.get_command(command_name)
        if command:
            embed = discord.Embed(title=f"Command: {command.name}", description=command.help, color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Command '{command_name}' not found.")


@bot.command()
async def entry(ctx, contract, network="eth"):
    """.entry <pool_contract> - Enters token into GoogleSheets. Requires a pool contract, a token contract will not
    work. If the entry exists, it is possible to overwrite existing entries too."""
    await ctx.typing()
    global token_bucket

    # Check if there are enough tokens in the bucket
    if token_bucket >= 1:
        # Consume a token and execute the command
        token_bucket -= 1

    # Authenticate Google Sheets
    service = gs.authenticate()

    # Call the merged function to fetch and extract data
    extracted_data = await gt.fetch_and_extract_information(network, contract)

    if not extracted_data:
        await ctx.send(f"""
{ctx.author.mention} - Failed to fetch data for Contract: **{contract}**

Please note, the ".entry" command only works with pool contracts, not token contracts.

If you don't know the pool address, retrieve it from https://www.geckoterminal.com/  using the token contact and try again with **".entry <pool_contract>"**.
""")
        return

    symbol, base_token_price_usd, reserve_in_usd, fdv_usd, contract, date, pool_address = await extract_data_fields(
        extracted_data)

    # Check if the entry exists in Google Sheets
    exists = gs.entry_exists(service, contract)  # Remove "await" here

    # Determine the embed formatting based on entry existence
    if exists:
        embed = fm.format_overwrite_entry(
            contract, symbol, base_token_price_usd, reserve_in_usd, fdv_usd, pool_address
        )
    else:
        embed = fm.format_entry_embed(
            contract, symbol, base_token_price_usd, reserve_in_usd, fdv_usd, pool_address
        )

    # Send the prompt message
    prompt_message = await ctx.send(embed=embed)
    await prompt_message.add_reaction("1️⃣")
    await prompt_message.add_reaction("2️⃣")

    def reaction_check(reaction, user):
        return user == ctx.author and reaction.message.id == prompt_message.id

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=60.0, check=reaction_check)

        if str(reaction.emoji) == "1️⃣":
            if exists:
                # Entry exists, handle overwrite logic
                try:
                    success = gs.add_entry_to_sheets(service, contract, date, symbol, base_token_price_usd, fdv_usd, reserve_in_usd, pool_address, overwrite=True)  # Remove "await" here

                    if success:
                        await ctx.send(f"@everyone - **${symbol}** updated in Google Sheets.")
                    else:
                        await ctx.send(f"{ctx.author.mention} - Failed to update {contract} in Google Sheets.")
                except Exception as e:
                    await ctx.send(f"{ctx.author.mention} - An error occurred while updating the entry in Google "
                                   f"Sheets: {str(e)}")
            else:
                # Entry does not exist, add it normally
                result = gs.add_entry_to_sheets(service, contract, date, symbol, base_token_price_usd, fdv_usd, reserve_in_usd, pool_address)  # Remove "await" here

                if result:
                    await ctx.send(f"@everyone - **${symbol}** added to Google Sheets. Use \"**.p {symbol}**\"\n"
                                   f" to view.")
                else:
                    await ctx.send(f"{ctx.author.mention} - Failed to add entry for {contract} to Google Sheets.")

        elif str(reaction.emoji) == "2️⃣":
            # User reacted with Emoji 2, don't add the entry to Google Sheets
            await ctx.send(f"{ctx.author.mention} - Entry for **${symbol}** not added to Google Sheets.")

        # Delete the prompt message
        await prompt_message.delete()

    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention} - No response. Entry not added to Google Sheets.")


@bot.command()
async def p(ctx, token_symbol):
    """.p <ticker> - Checks the live price of a token in Google sheets."""
    await ctx.typing()
    global token_bucket

    # Check if there are enough tokens in the bucket
    if token_bucket >= 1:
        # Consume a token and execute the command
        token_bucket -= 1

    # Authenticate Google Sheets
    service = gs.authenticate()

    # Check if the ticker exists in Google Sheets
    pool_contract = await asyncio.to_thread(gs.get_pool_contract, service, token_symbol)

    if pool_contract:
        # Fetch live token price data from Gecko Terminal using the pool contract
        extracted_data = await gt.fetch_and_extract_information("eth", pool_contract)  # Adjust the network if needed

        if extracted_data and "base_token_price_usd" in extracted_data:
            # Convert base_token_price_usd to a float (if it's not already)
            base_token_price_usd = float(extracted_data["base_token_price_usd"])
            await ctx.send(f"The live price of **${token_symbol.upper()}** is ${base_token_price_usd:.8f}.")
        else:
            # Error fetching live price
            await ctx.send(f"Error fetching the live price of {token_symbol.upper()} from Gecko Terminal.")
    else:
        # Ticker not found in Google Sheets
        await ctx.send(f"{ctx.author.mention} - Ticker {token_symbol.upper()} not found in Google Sheets.")


@bot.command()
async def remove(ctx, token_symbol):
    """.remove <ticker> - Removes an entry from GoogleSheets."""
    await ctx.typing()
    global token_bucket

    # Check if there are enough tokens in the bucket
    if token_bucket >= 1:
        # Consume a token and execute the command
        token_bucket -= 1

    # Convert the user input to uppercase
    token_symbol = token_symbol.upper()

    # Authenticate Google Sheets
    service = gs.authenticate()

    # Check if the ticker exists in Google Sheets
    exists = await asyncio.to_thread(gs.get_pool_contract, service, token_symbol)

    if not exists:
        await ctx.send(f"{ctx.author.mention} - Entry for '{token_symbol}' not found in Google Sheets.")
        return

    # Fetch and extract data for the token symbol
    pool_contract = await asyncio.to_thread(gs.get_pool_contract, service, token_symbol)

    if not pool_contract:
        await ctx.send(f"{ctx.author.mention} - Failed to fetch pool contract for Token Symbol: **{token_symbol}**")
        return

    # Fetch and extract data for the pool_contract
    extracted_data = await gt.fetch_and_extract_information("eth", pool_contract)  # Adjust the network if needed

    if not extracted_data:
        await ctx.send(f"{ctx.author.mention} - Failed to fetch data for Pool Contract: **{pool_contract}**")
        return

    # Use the extract_data_fields function to extract data fields
    symbol, base_token_price_usd, reserve_in_usd, fdv_usd, contract, date, pool_address = await extract_data_fields(extracted_data)

    # Determine the embed formatting for the prompt message
    embed = fm.format_remove_entry(token_symbol, symbol, base_token_price_usd, reserve_in_usd, fdv_usd, pool_address)

    # Send the prompt message
    prompt_message = await ctx.send(embed=embed)
    await prompt_message.add_reaction("1️⃣")
    await prompt_message.add_reaction("2️⃣")

    def reaction_check(reaction, user):
        return user == ctx.author and reaction.message.id == prompt_message.id

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=60.0, check=reaction_check)

        if str(reaction.emoji) == "1️⃣":
            # Entry exists, remove it
            success = gs.remove_entry_from_sheets(service, token_symbol)  # Use your existing function to remove based on token symbol

            if success:
                await ctx.send(f"@everyone - Entry for '{token_symbol}' removed from Google Sheets.")
            else:
                await ctx.send(f"{ctx.author.mention} - Failed to remove entry for '{token_symbol}' from Google Sheets.")

        elif str(reaction.emoji) == "2️⃣":
            # User reacted with Emoji 2, don't remove the entry
            await ctx.send(f"{ctx.author.mention} - Entry for '{token_symbol}' not removed from Google Sheets.")

        # Delete the prompt message
        await prompt_message.delete()

    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention} - No response. Entry for '{token_symbol}' not removed from Google Sheets.")


@bot.command()
async def clear(ctx, amount: int = 5):
    """.clear <int> - Takes a number between 1 and 100 and deletes that amount of messages"""
    await ctx.typing()
    global token_bucket

    # Check if there are enough tokens in the bucket
    if token_bucket >= 1:
        # Consume a token and execute the command
        token_bucket -= 1

    if ctx.author.guild_permissions.manage_messages:  # Check if the user has permission to manage messages
        if amount < 1 or amount > 100:  # Limit the number of messages to be between 1 and 100
            await ctx.send("Please provide a number between 1 and 100.")
        else:
            await ctx.channel.purge(limit=amount + 1)  # Delete the specified number of messages
            await ctx.send(f"{ctx.author.mention}, {amount} messages deleted.", delete_after=5)
    else:
        await ctx.send("You don't have permission to manage messages.")


def start_bot(token):
    bot.run(token)


if __name__ == "__main__":
    start_bot(config.token)

