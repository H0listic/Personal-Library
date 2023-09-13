import discord


def format_entry_embed(token_address, symbol, base_token_price_usd, reserve_in_usd, fdv_usd, pool_address):
    try:
        # Convert integer values to floats or decimals
        base_token_price_usd = float(base_token_price_usd)
        reserve_in_usd = float(reserve_in_usd)
        fdv_usd = float(fdv_usd)

        embed = discord.Embed(
            title="${} - ${:.8f}".format(symbol, base_token_price_usd),
            description="--------------------",
            color=0x00ff00
        )

        embed.add_field(name="Liquidity", value="${:,.2f}".format(reserve_in_usd), inline=False)
        embed.add_field(name="FDV", value="${:,.2f}".format(fdv_usd), inline=False)
        embed.add_field(name="Token address", value=token_address, inline=False)
        embed.add_field(name="Pool address", value=pool_address, inline=False)
        embed.add_field(name="Would you like to add the above token to Google sheets?",
                        value="""Tap 1️⃣ for yes :white_check_mark:
                        Tap 2️⃣ for no   :x:
                        """)

    except ValueError as e:
        # Handle the case where one of the values is not a valid number
        embed = discord.Embed(
            title="Invalid Data",
            description="The data for this entry is not valid.",
            color=0xff0000  # Red color for error
        )

    return embed


def format_overwrite_entry(token_address, symbol, base_token_price_usd, reserve_in_usd, fdv_usd, pool_address):
    try:
        # Convert integer values to floats or decimals
        base_token_price_usd = float(base_token_price_usd)
        reserve_in_usd = float(reserve_in_usd)
        fdv_usd = float(fdv_usd)
        pool_address = pool_address

        embed = discord.Embed(
            title="The following token already exists. Would you like to overwrite it?",
            description="""--------------------""",
            color=0x00ff00
        )

        embed.add_field(name="Token Symbol", value=f"${symbol}", inline=False)
        embed.add_field(name="Liquidity", value="${:,.2f}".format(reserve_in_usd), inline=False)
        embed.add_field(name="FDV", value="${:,.2f}".format(fdv_usd), inline=False)
        embed.add_field(name="Token address", value=token_address, inline=False)
        embed.add_field(name="Overwrite existing entry?",
                        value="""Tap 1️⃣ for yes :white_check_mark:
                                Tap 2️⃣ for no   :x:
                                """)

    except ValueError as e:
        # Handle the case where one of the values is not a valid number
        embed = discord.Embed(
            title="Invalid Data",
            description="The data for this entry is not valid.",
            color=0xff0000  # Red color for error
        )

    return embed


def format_remove_entry(token_address, symbol, base_token_price_usd, reserve_in_usd, fdv_usd, pool_address):
    try:
        # Convert integer values to floats or decimals
        token_address = token_address
        pool_address = pool_address
        base_token_price_usd = float(base_token_price_usd)
        reserve_in_usd = float(reserve_in_usd)
        fdv_usd = float(fdv_usd)

        embed = discord.Embed(
            title="""**${}** - **${:,.8f}**
Token found, are you sure you want to remove it?""".format(symbol, base_token_price_usd),
            description="""--------------------""",
            color=0x00ff00
        )

        embed.add_field(name="Liquidity", value="${:,.2f}".format(reserve_in_usd), inline=False)
        embed.add_field(name="FDV", value="${:,.2f}".format(fdv_usd), inline=False)
        embed.add_field(name="Token address", value=token_address, inline=False)
        embed.add_field(name="Pool address", value=pool_address, inline=False)
        embed.add_field(name="Remove entry?",
                        value="""Tap 1️⃣ for yes :white_check_mark:
                                Tap 2️⃣ for no   :x:
                                """)

    except ValueError as e:
        # Handle the case where one of the values is not a valid number
        embed = discord.Embed(
            title="Invalid Data",
            description="The data for this entry is not valid.",
            color=0xff0000  # Red color for error
        )

    return embed











