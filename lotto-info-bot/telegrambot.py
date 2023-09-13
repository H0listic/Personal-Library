import asyncio
import telegram
import config
import webthree
import formatting
import contract_abi
from telegram.constants import ParseMode
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


channel_id = "-1001961939059"
group_channel_id = "-1001924602600"


async def send_periodic_lottery_details(bot, channel_id, contract, current_lottery_id):
    w3 = await webthree.connect_to_chain()

    while True:
        try:
            # Ensure we have the most up-to-date current_lottery_id
            current_lottery_id = await webthree.retrieve_lottery_id(w3)

            if current_lottery_id is not None:
                # Initialize the contract object inside the loop with the correct Web3 instance
                contract = w3.eth.contract(address=webthree.CONTRACT_ADDRESS, abi=contract_abi.ABI)

                # Get the lottery details
                lottery_details = await webthree.get_lottery_details(w3)

                if lottery_details is not None:
                    # Format the lottery details using the formatting function
                    message = formatting.format_lottery_details(lottery_details)

                    # Send the message to the admin channel
                    await bot.send_message(chat_id=channel_id, text=message, parse_mode=ParseMode.MARKDOWN,
                                           disable_web_page_preview=True)

                    # Send the message to the group channel
                    await bot.send_message(chat_id=group_channel_id, text=message, parse_mode=ParseMode.MARKDOWN,
                                           disable_web_page_preview=True)

                    print("Lottery details sent successfully.")
                else:
                    pass
                    print("Failed to retrieve lottery details.")
            else:
                pass
                print("Failed to retrieve current lottery ID.")

        except Exception as e:
            pass
            print(f"Error sending lottery details: {e}")

        # Wait for 1 hour (3600 seconds) before sending the next message
        await asyncio.sleep(1800)


async def fetch_prize_pool_background(CONTRACT_ADDRESS, ARBWETH):
    while True:
        try:
            # Fetch the prize pool in the background
            balance = await formatting.fetch_prize_pool(CONTRACT_ADDRESS, ARBWETH)
            print(f"Prize pool updated: {balance} GWEI")
        except Exception as e:
            print(f"Error fetching prize pool: {e}")

        # Wait for 1 minute (60 seconds) before fetching again
        await asyncio.sleep(60)


async def lottery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the formatted lottery details when the /lottery command is issued."""
    w3 = await webthree.connect_to_chain()
    if w3:
        contract = w3.eth.contract(address=webthree.CONTRACT_ADDRESS, abi=contract_abi.ABI)
        lottery_details = await webthree.get_lottery_details(w3)
        if lottery_details is not None:
            message = formatting.format_lottery_details(lottery_details)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )


async def main():
    bot = telegram.Bot(config.tg_Token)
    w3 = await webthree.connect_to_chain()  # Await to get the Web3 instance

    if w3:
        contract = w3.eth.contract(address=webthree.CONTRACT_ADDRESS, abi=contract_abi.ABI)
        current_lottery_id = None  # Initialize current_lottery_id here

        # Create the Application instance and pass it your bot's token.
        application = Application.builder().token(config.tg_Token).build()

        # Add the /lottery command handler
        application.add_handler(CommandHandler("lottery", lottery))

        # Create tasks for both sending lottery details and fetching prize pool
        fetch_prize_pool_task = asyncio.create_task(
            fetch_prize_pool_background(formatting.CONTRACT_ADDRESS, formatting.ARBWETH)
        )
        send_lottery_details_task = asyncio.create_task(
            send_periodic_lottery_details(bot, channel_id, contract, current_lottery_id)
        )

        # Wait for both tasks to complete
        await asyncio.gather(send_lottery_details_task, fetch_prize_pool_task)


if __name__ == '__main__':
    asyncio.run(main())

