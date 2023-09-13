from datetime import datetime
import contract_abi
import asyncio
import webthree
import config
from web3 import Web3


CONTRACT_ADDRESS = "0xb05c8C6bbE2Cd46F6d8cE3938730A4c726a62E58"
ARBWETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
PRIZE_POOL = 0


async def fetch_prize_pool(CONTRACT_ADDRESS, ARBWETH):
    global PRIZE_POOL

    while True:
        try:
            web3 = Web3(Web3.HTTPProvider(config.arbMain))
            token_abi = contract_abi.WETH_ABI
            token_contract = web3.eth.contract(address=ARBWETH, abi=token_abi)
            balance = token_contract.functions.balanceOf(CONTRACT_ADDRESS).call()

            # Update PRIZE_POOL with the new value & convert from GWEI to WETH
            PRIZE_POOL = balance / 10 ** 18  
            # print(PRIZE_POOL)

            # Check once per minute for changes to PRIZE_POOL
            await asyncio.sleep(60)
        except Exception as e:
            print(f"Error fetching prize pool: {e}")


def format_lottery_details(lottery_details):
    # Convert Unix timestamps to human-readable date and time
    start_time = datetime.utcfromtimestamp(lottery_details[1]).strftime('%y-%m-%d %H:%M')
    end_time = datetime.utcfromtimestamp(lottery_details[2]).strftime('%y-%m-%d %H:%M')
# ╔═════๑♡๑═════╗
    message = f"""
𝗟░𝗢░𝗧░𝗧░𝗘░𝗥░𝗬░░𝗜░𝗡░𝗙░𝗢
**╔═════════ ⇦♕⇨ ═════════╗**
\U0001F4CD **-** Arbitrum
\U0001F3B2 **-** Lottery No. {webthree.CURRENT_LOTTERY_ID}
\U00002705 **-** Started: {start_time} UTC
\U0000274C **-** Ends: {end_time} UTC
\U0001F4B0 **-** Prize Pot: {PRIZE_POOL:.2f} $ETH
\U0001F39F **-** Ticket Price: 0.0025 $ETH
**╚═══════════════════════╝**
[Buy tickets!](https://app.0xlotto.games/) (Arbitrum)
**━━━━━━━━━━━━━━━━━━━━━━━━━**
[Buy $LOTTO](https://app.uniswap.org/#/swap?inputCurrency=eth&outputCurrency=0xf47ab324910c4017af6f30411e31bc26cac90648) (Ethereum)
**◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇**
[Telegram](https://t.me/+mFF98Repk6s5NGMx) | [Website](https://linktr.ee/0xLotto)
"""

    return message


if __name__ == "__main__":
    asyncio.run(fetch_prize_pool(CONTRACT_ADDRESS, ARBWETH))
