import ccxt.pro as ccxtpro
import ccxt
import time
import asyncio
from pprint import pprint
import pandas as pd

bybit = ccxt.bybit({
    'apiKey': 'key',
    'secret': 'secret',
})

position_list = []

autotest_main_log = pd.DataFrame(
    columns=['Date', 'Day', 'Symbol', 'Side', '฿ Size', '$ Size', 'Entry', 'Target', 'Stop', 'Exit', 'Fee', 'P&L',
             'Risk $', 'R Multiple', '% Wins', ])

while True:
    positions = bybit.fetch_positions()

    for position in positions:
        if len(positions) == 0:
            time.sleep(15)
        else:
            symbol = position['info']['symbol']

            if symbol not in [p['info']['symbol'] for p in position_list]:
                print(f"New position added: {symbol}")
                date = pd.to_datetime(position['info']['createdTime'], unit='ms').strftime('%d/%m/%Y %H:%M')
                day = pd.to_datetime(date).day_name()
                side = position['side']
                size = position['info']['size']
                entry = position['info']['entryPrice']
                dollar_size = f"${float(size) * float(entry)}"
                stop = position['info']['stopLoss']
                fee = position['info']['occClosingFee']

                # Check if a row with the same symbol, side, entry and stop values already exists in the dataframe
                mask = (autotest_main_log['Symbol'] == symbol) & (autotest_main_log['Side'] == side) & \
                       (autotest_main_log['Entry'] == entry) & (autotest_main_log['Stop'] == stop)

                if mask.any():
                    # Update the existing row with the latest information
                    autotest_main_log.loc[mask,
                    ['Date', 'Day', '฿ Size', '$ Size', 'Fee']] = [date, day, size, dollar_size, fee]
                else:
                    # Add a new row to the dataframe
                    new_row = pd.DataFrame({
                        'Date': [date],
                        'Day': [day],
                        'Symbol': [symbol],
                        'Side': [side],
                        '฿ Size': [size],
                        '$ Size': [dollar_size],
                        'Entry': [entry],
                        'Target': [''],
                        'Stop': [stop],
                        'Exit': [''],
                        'Fee': [fee],
                        'P&L': [''],
                        'Risk $': [''],
                        'R Multiple': [''],
                        '% Wins': ['']
                    })

                    autotest_main_log = pd.concat([autotest_main_log, new_row], ignore_index=True)
            else:
                stop_loss = position['info']['stopLoss']
                for p in position_list:
                    if p['info']['symbol'] == symbol and p['info']['stopLoss'] != stop_loss:
                        p['info']['stopLoss'] = stop_loss
                        print(f"Stop loss updated for {symbol} position: {p}")

            print(autotest_main_log.head())

    time.sleep(15)
