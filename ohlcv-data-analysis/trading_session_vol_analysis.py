import pandas as pd
from datetime import datetime

# Read in the BTC OHLCV data from a CSV file
df = pd.read_csv("/home/fam/Documents/BITSTAMP_BTCUSD_1HR.csv")

# Create columns for the London, New York, and Asian trading sessions
df['London'] = 0
df['New York'] = 0
df['Asia'] = 0

# Create columns for the London, New York, and Asian trading session volume averages.
df["London Average"] = 0
df["New York Averages"] = 0
df["Asian Averages"] = 0

# Convert the unix time to datetime in new column
df['datetime'] = df['time'].apply(datetime.fromtimestamp)

# Define the trading session hours.
trading_hours = {
    'London': {'open': '7', 'close': '16'},
    'New York': {'open': '12', 'close': '21'},
    'Asian': {'open': '23', 'close': '8'},
}

# Create a numeric hour column
df['hour'] = df['datetime'].dt.hour
print(df)

for index, row in df.iterrows():
    hour = row['hour']

    london_open = int(trading_hours['London']['open'])
    london_close = int(trading_hours['London']['close'])
    if london_open <= hour < london_close:
        df.loc[index, 'London'] += 1

    new_york_open = int(trading_hours['New York']['open'])
    new_york_close = int(trading_hours['New York']['close'])
    if new_york_open <= hour < new_york_close:
        df.loc[index, 'New York'] += 1

    # asian_open = int(trading_hours['Asian']['open'])
    # asian_close = int(trading_hours['Asian']['close'])
    # select rows where the 'hour' column is equal to 23
    # select rows where the 'hour' column is equal to 23
    selected_rows = df.loc[df['hour'] == 23]

    # get the start and stop index values of the selected rows
    start_index = df.index.start
    stop_index = df.index.stop

    # select the next 9 rows after the selected rows
    next_9_rows = df.iloc[start_index + 1: stop_index + 10]

    # create a copy of the next_9_rows dataframe
    next_9_rows_copy = next_9_rows.copy()

    # set the value of the selected rows to 1
    next_9_rows['hour'] = 1
    # if df.loc[df['hour']] == 23:
    # asian_session = df.loc[df['hour'] == 23]


print(df.loc[:50, 'London'])
print(df.loc[:50, 'New York'])
print(df.loc[:50, 'Asia'])
