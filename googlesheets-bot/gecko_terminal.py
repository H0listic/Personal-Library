import aiohttp
import asyncio
from pprint import pprint
from datetime import datetime


async def get_attribute_value(data, key):
    return data.get("data", {}).get("attributes", {}).get(key)


async def fetch_and_extract_information(network, pool_address):
    base_url = "https://api.geckoterminal.com/api/v2/networks/"
    endpoint = f"pools/{pool_address}?include=base_token%2C%20quote_token%2C%20dex"

    # Define header specifying the API version
    headers = {
        "Accept": "application/json;version=20230302",  # Replace with the desired API version
    }

    async with aiohttp.ClientSession() as session:
        url = f"{base_url}{network}/{endpoint}"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    if data:
                        # pprint(data)
                        # attributes = data.get("data", {}).get("attributes", {})
                        included = data.get("included", [])

                        base_token_price_usd = await get_attribute_value(data, "base_token_price_usd")
                        reserve_in_usd = await get_attribute_value(data, "reserve_in_usd")
                        fdv_usd = await get_attribute_value(data, "fdv_usd")
                        pool_address = await get_attribute_value(data, "address")

                        # base_token_price_usd = attributes.get("base_token_price_usd")
                        # reserve_in_usd = attributes.get("reserve_in_usd")
                        # fdv_usd = attributes.get("fdv_usd")
                        # pool_address = attributes.get("address")
                        # # volume = attributes.get("volume_usd")

                        token_info = next((item.get("attributes") for item in included if item.get("type") == "token"),
                                          {})

                        symbol = token_info.get("symbol")
                        token_contract = token_info.get("address")

                        # Get current UTC time and format as a string
                        date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

                        extracted_data = {
                            "base_token_price_usd": base_token_price_usd,
                            "reserve_in_usd": reserve_in_usd,
                            "fdv_usd": fdv_usd,
                            "symbol": symbol,
                            "contract": token_contract,
                            "timestamp": date,
                            "pool_address": pool_address
                        }

                        return extracted_data
                    else:
                        return None  # No data retrieved
                else:
                    # Handle errors here, e.g., raise an exception or return an error message
                    return None
        except aiohttp.ClientError as e:
            # Handle network errors here
            return None

# if __name__ == "__main__":
#     network = "eth"  # Replace with your desired network
#     pool_address = "0x3ac4b2c0cbb85d309f1a7d0410e8e10594e5c928"  # Replace with your pool address
#
#     loop = asyncio.get_event_loop()
#     data = loop.run_until_complete(fetch_and_extract_information(network, pool_address))
