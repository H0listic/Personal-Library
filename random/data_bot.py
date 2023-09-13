import os
import logging
import asyncio
import ccxt
import pandas as pd
from pycoingecko import CoinGeckoAPI
from aiogram import types
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.contrib.middlewares.logging import LoggingMiddleware

cg = CoinGeckoAPI()

# Replace YOUR_BOT_TOKEN with your actual bot token
API_TOKEN = "token" # replace with api token

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def handle_channel_update(message: types.Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    # Check if the chat ID is already in the file
    if not is_chat_id_in_file(chat_id):
        # If not, add it to the file
        with open("channels.txt", "a") as f:
            f.write(f"{chat_id},{chat_title}\n")

async def is_chat_id_in_file(chat_id: int) -> bool:
    if not os.path.exists("channels.txt"):
        return False

    with open("channels.txt", "r") as f:
        for line in f:
            stored_chat_id, _ = line.strip().split(",", 1)
            if int(stored_chat_id) == chat_id:
                return True

    return False

async def list_channels(message: types.Message):
    if not os.path.exists("channels.txt"):
        await message.reply("The bot is not in any channels.")
        return

    with open("channels.txt", "r") as f:
        channels = [line.strip().split(",", 1) for line in f]

    response = "The bot is in the following channels:\n\n"
    for chat_id, chat_title in channels:
        response += f"{chat_title} (ID: {chat_id})\n"

    await message.reply(response)

# Register handlers
dp.register_message_handler(handle_channel_update, content_types=['new_chat_members'])
dp.register_message_handler(list_channels, Command("listchannels"))

def get_coin_data(ticker):
    coin_data = cg.get_coin_by_id(ticker.lower())
    name = coin_data['name']
    symbol = coin_data['symbol'].upper()
    rank = coin_data['market_cap_rank']
    usd_price = coin_data['market_data']['current_price']['usd']
    high_24h = coin_data['market_data']['high_24h']['usd']
    low_24h = coin_data['market_data']['low_24h']['usd']
    btc_price = coin_data['market_data']['current_price']['btc']
    eth_price = coin_data['market_data']['current_price']['eth']
    hr1_change = coin_data['market_data']['price_change_percentage_1h_in_currency']['usd']
    day_change = coin_data['market_data']['price_change_percentage_24h']
    week_change = coin_data['market_data']['price_change_percentage_7d']
    volume = coin_data['market_data']['total_volume']['usd']
    volume_1h = coin_data['market_data']['total_volume']['usd'] * (1 + hr1_change / 100)
    volume_24h = coin_data['market_data']['total_volume']['usd'] * (1 + day_change / 100)
    market_cap = coin_data['market_data']['market_cap']['usd']

    menu = f"""
+--------------------------------------+
| {symbol} - {name} - #{rank}{" "*(25-len(name)-len(symbol)-len(str(rank)))}|
+--------------------------------------+
| Price (USD):         ${usd_price:,.0f}{" "*(12-len(f"{usd_price:,.0f}"))}|
| H: ${high_24h:,.0f}{" "*(10-len(f"{high_24h:,.0f}"))}| L: ${low_24h:,.0f}{" "*(10-len(f"{low_24h:,.0f}"))}|
| Price (BTC):                {btc_price:.8f}{" "*(10-len(f"{btc_price:.8f}"))}|
| Price (ETH):                 {eth_price:.2f}{" "*(10-len(f"{eth_price:.2f}"))}|
| 1hr:                  {hr1_change:+.2f}%{" "*(10-len(f"{hr1_change:+.2f}"))}|
| 24hr:                 {day_change:+.2f}%{" "*(10-len(f"{day_change:+.2f}"))}|
| 1w:                   {week_change:+.2f}%{" "*(10-len(f"{week_change:+.2f}"))}|
| Vol:            ${volume:,.0f}{" "*(12-len(f"{volume:,.0f}"))}|
| 1hr Vol:           ${volume_1h:,.0f}{" "*(12-len(f"{volume_1h:,.0f}"))}|
| 24hr Vol:          ${volume_24h:,.0f}{" "*(12-len(f"{volume_24h:,.0f}"))}|
| Mcap:   ${market_cap:,.0f}{" "*(12-len(f"{market_cap:,.0f}"))}|
+--------------------------------------+
|          - CoinGecko API -           |
+--------------------------------------+
"""
    return menu

async def process_command(ticker):
    def coin_exists(ticker):
        coins_list = cg.get_coins_list()
        return any(coin for coin in coins_list if coin['symbol'].lower() == ticker.lower())

    if coin_exists(ticker):
        try:
            menu = await get_coin_data(ticker)
            return menu
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Error: Coin not found"


# Handler for the start command
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hi! Send me a message in the format '.p {ticker}' to get general coin data.")

# Handler for the help command
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Send me a message in the format '.p {ticker}' to get general coin data.")

# Handler for processing user messages
@dp.message_handler(lambda message: message.text.lower().startswith(".p "))
async def handle_message(message: types.Message):
    if message.text.lower().startswith(".p "):
        ticker = message.text[3:].strip()
        if ticker.isalnum():  # Check if the input ticker is alphanumeric
            try:
                coin_data = cg.get_coin_by_id(ticker, localization=False)
                if coin_data is not None:
                    menu = await process_command(ticker)
                    await message.reply(menu, parse_mode=ParseMode.MARKDOWN)
                else:
                    await message.reply(f"Error: {ticker.upper()} is not listed on CoinGecko.")
            except Exception as e:
                await message.reply(f"Error: {e}")
        else:
            await message.reply("Invalid input. Please provide a valid ticker.")


# Error handler
async def on_startup(dp):
    await bot.send_message(chat_id=-1001273610629, text="Bot has been started")

async def on_shutdown(dp):
    await bot.send_message(chat_id=-1001273610629, text="Bot has been stopped")

    await bot.close()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
