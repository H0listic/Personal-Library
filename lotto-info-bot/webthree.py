import asyncio
from web3 import Web3
import telegram
import contract_abi
import config

# Replace with your contract ABI and address
CONTRACT_ABI = contract_abi.ABI
CONTRACT_ADDRESS = "0xb05c8C6bbE2Cd46F6d8cE3938730A4c726a62E58"
ARBWETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
CURRENT_LOTTERY_ID = None

# Initialize the Telegram bot
bot = telegram.Bot(config.tg_Token)


async def connect_to_chain():
    try:
        w3 = Web3(Web3.HTTPProvider(config.arbMain))

        # Check if connected successfully
        if w3.is_connected():
            print("Connected to Blockchain mainnet successfully.")
            return w3
        else:
            print("Failed to connect to Ethereum mainnet.")
            return None

    except Exception as e:
        print(f"Connection error: {e}")
        return None


async def retrieve_lottery_id(w3):
    if w3 is None:
        print("Cannot retrieve contract data without a valid Web3 instance.")
        return

    try:
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi.ABI)

        # Fetch current lottery ID and update Global variable if necessary
        new_lottery_id = contract.functions.viewCurrentLotteryId().call()
        print(f'Updated lottery ID to {new_lottery_id}')

        global CURRENT_LOTTERY_ID
        CURRENT_LOTTERY_ID = new_lottery_id

        return new_lottery_id

    except Exception as e:
        pass
        print('Error calling viewCurrentLotteryId:', str(e))
    return None


async def get_lottery_details(w3):
    try:
        # Ensure we have the most up-to-date current_lottery_id
        current_lottery_id = await retrieve_lottery_id(w3)

        # Retrieve lottery details based on the current lottery ID using the contract instance
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi.ABI)
        lottery_details = contract.functions.viewLottery(current_lottery_id).call()

        print('Lottery Details:', lottery_details)
        return lottery_details
    except Exception as e:
        print('Error calling viewLottery:', str(e))


async def run_periodic_task():
    while True:
        await main()  on
        await asyncio.sleep(3600)


async def main():
    w3_instance = await connect_to_chain()

    if w3_instance:
        await get_lottery_details(w3_instance)


if __name__ == "__main__":
    asyncio.run(run_periodic_task())




