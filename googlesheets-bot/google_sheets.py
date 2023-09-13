import os
import asyncio
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "spreadsheet_id"


def authenticate():
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not credentials or not credentials.valid:
        try:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                credentials = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(credentials.to_json())
        except Exception as e:
            print(f"Error during authentication: {e}")
            return None  # Return None to indicate authentication failure

    return build("sheets", "v4", credentials=credentials)


def get_values_from_spreadsheet(service, range_name):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        values = result.get("values", [])
        return values

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def entry_exists(service, contract):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A2:A1000"  # Check column A for the contract
        ).execute()
        values = result.get("values", [])

        if values:
            for row in values:
                if row and row[0].strip() == contract.strip():
                    return True

        return False  # Contract not found in column A

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def add_entry_to_sheets(service, token_contract, date, symbol, base_token_price_usd, fdv_usd, reserve_in_usd,
                        pool_address, overwrite=False):
    try:
        # Check if the entry already exists in column A
        if entry_exists(service, token_contract):
            return False  # Entry already exists, no need to add it again

        # If it doesn't exist, add the entry
        range_name = "Sheet1!A2:A1000"
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        values = result.get("values", [])

        # Find the first empty cell in column A
        next_row = len(values) + 2  # Add 2 to account for header and 1-based indexing

        # Construct the values to update in the row
        row_values = [
            [token_contract, date, symbol, base_token_price_usd, '', '', '', fdv_usd, reserve_in_usd, '', '', '',
             '', '', '', '', '', '', pool_address]
        ]

        # Check if the contract already exists
        for index, row in enumerate(values):
            if row and row[0].strip() == token_contract.strip():
                # Contract already exists, update the existing row
                next_row = index + 2  # Use the index of the existing row

        # Write entry to sheets, update multiple cells in the same row
        range_name = f"Sheet1!A{next_row}:S{next_row}"  # Update from A to S in the same row
        value_input_option = "RAW"
        body = {"values": row_values}

        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption=value_input_option,
            body=body
        ).execute()

        return True  # Return True to indicate successful update

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def get_pool_contract(service, token_symbol):
    try:
        # Search Column C for Symbols
        range_name = f"Sheet1!C2:C1000"
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        values = result.get("values", [])

        # Search for the token symbol in column C and return the corresponding pool contract from column S
        for row in values:
            if row and row[0].strip().lower() == token_symbol.strip().lower():
                # Get the corresponding pool contract from column S
                row_index = values.index(row)
                pool_contract_range = f"Sheet1!S{row_index + 2}"  # Adjust for 1-based indexing
                pool_contract_result = service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=pool_contract_range
                ).execute()
                pool_contract_value = pool_contract_result.get("values", [])

                if pool_contract_value:
                    return pool_contract_value[0][0]

        return None  # Token symbol not found in column C

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def remove_entry_from_sheets(service, ticker_or_contract):
    try:
        # Check if the entry exists in column A and column C
        range_name_a = f"Sheet1!A2:A1000"
        range_name_c = f"Sheet1!C2:C1000"

        result_a = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name_a
        ).execute()

        result_c = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name_c
        ).execute()

        values_a = result_a.get("values", [])
        values_c = result_c.get("values", [])

        # Find the row where the ticker_or_contract exists in either column A or C
        row_to_remove = None
        for i, (row_a, row_c) in enumerate(zip(values_a, values_c)):
            if (row_a and row_a[0].strip() == ticker_or_contract.strip()) or (
                    row_c and row_c[0].strip() == ticker_or_contract.strip()):
                row_to_remove = i + 2  # Add 2 for 1-based indexing and header row
                break

        if row_to_remove is not None:
            print(f"Removing row {row_to_remove} for {ticker_or_contract}")  # Debugging statement
            # Remove the entire row
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={
                    "requests": [
                        {
                            "deleteDimension": {
                                "range": {
                                    "sheetId": 0,  # Assuming the sheet has ID 0
                                    "dimension": "ROWS",
                                    "startIndex": row_to_remove - 1,  # 0-based index
                                    "endIndex": row_to_remove  # Inclusive
                                }
                            }
                        }
                    ]
                }
            ).execute()

            if 'error' in response:
                print(f"Error removing row: {response['error']['message']}")  # Print error message
                return False
            else:
                return True  # Return True to indicate successful removal
        else:
            print(f"No row found for {ticker_or_contract}")  # Debugging statement
            return False  # Ticker/Contract not found in column A or C

    except HttpError as error:
        print(f"HTTP Error occurred: {error}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# def get_all_entries(service, ticker):
#     try:
#         # Check tickers in column C
#         range_name_c = f"Sheet1!C2:C1000"
#
#         result = service.spreadsheets().values().get(
#             spreadsheetId=SPREADSHEET_ID,
#             range=range_name_c
#         ).execute()
#
#         values = result.get('values', [])
#
#         if values:
#             # Create list of dict
#             entries =[]
#             for row in values:
#                 entry = {
#                     'symbol'
#                 }



