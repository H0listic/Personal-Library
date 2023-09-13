import pandas as pd
import datetime

# Read the csv file into a dataframe
df = pd.read_csv('/home/fam/database/Projects/trading/OHLCV_csv/BITSTAMP_BTCUSD_1D_OHLCV.csv')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')

# Extract the name of weekdays
df['dayofweek'] = df['date'].dt.day_name()
print(df)

# Create a new column called 'wo' for weekly open.
df['wo'] = 'NaN'

# Set the 'wo' value to the 'open' value if the 'dayofweek' value is 'Monday'
df.loc[df['dayofweek'] == 'Monday', 'wo'] = df['open']

# Create a new column 'touches_open'
df['touches_open'] = False

# Loop through each row in the dataframe
for i, row in df.iterrows():
    # If the 'dayofweek' value is 'Monday'
    if row['dayofweek'] == 'Monday':
        # Get the 'open' value
        open_value = row['open']

        # Check the next 6 rows to see if the 'open' value is touched
        for j in range(1, 7):
            # Check if the index of the current row plus j is within the bounds of the dataframe
            if i + j >= len(df):
                # If the index is out of bounds, break out of the inner loop
                continue

            # Check if the 'open' value of the current row is equal to the 'open' value of the next row
            if df.loc[i + j, 'open'] == open_value:
                # If the 'open' value is touched, set the 'touches_open' value to True
                df.loc[i, 'touches_open'] = True
                # Break out of the inner loop
                break

# Count total of each day of week
total_mondays = 0
total_tuesdays = 0
total_wednesdays = 0
total_thursdays = 0
total_fridays = 0
total_saturdays = 0
total_sundays = 0

for i in range(len(df)):
    if df['dayofweek'][i] == 'Monday':
        total_mondays = total_mondays + 1

    if df['dayofweek'][i] == 'Tuesday':
        total_tuesdays = total_tuesdays + 1

    if df['dayofweek'][i] == 'Wednesday':
        total_wednesdays = total_wednesdays + 1

    if df['dayofweek'][i] == 'Thursday':
        total_thursdays = total_thursdays + 1

    if df['dayofweek'][i] == 'Friday':
        total_fridays = total_fridays + 1

    if df['dayofweek'][i] == 'Saturday':
        total_saturdays = total_saturdays + 1

    if df['dayofweek'][i] == 'Sunday':
        total_sundays = total_sundays + 1


green_mondays = []
red_mondays = []
for i in range(len(df)):
    if df['dayofweek'][i] == 'Monday' and df['close'][i] > df['open'][i]:
        green_mondays.append(df['date'])

    elif df['dayofweek'][i] == 'Monday' and df['close'][i] < df['open'][i]:
        red_mondays.append(df['date'])

print(len(green_mondays))
print(len(red_mondays))


tuesday_touches_bull_monday_open = []
tuesday_touches_bear_monday_open = []
for i in range(len(df)):
    if df['dayofweek'][i] == 'Monday' and df['close'][i] > df['open'][i]:
        if df['dayofweek'][i + 1] and df['low'][i + 1] < df['open'][i]:
            tuesday_touches_bull_monday_open.append(df['date'][i])

    elif df['dayofweek'][i] == 'Monday' and df['close'][i] < df['open'][i]:
        if df['dayofweek'][i + 1] and df['high'][i + 1] > df['open'][i]:
            tuesday_touches_bear_monday_open.append(df['date'][i])

print(len(tuesday_touches_bull_monday_open))
print(len(tuesday_touches_bear_monday_open))



for i in range(len(df)):
    if df['dayofweek'][i] == 'Tuesday' and df['high'][i] > df['open'][i - 1]:
        tuesday_touches_bear_monday_open.append(df['date'][i])







# WEEKLY CANDLES
# # Iterate over the df and add 1s to wo
# for i, row in df.iterrows():
#     # Get previous close
#     prev_close = df.iloc[i-1, df.columns.get_loc('close')]
#
#     # Check if the current row's high value is greater than the previous rows close
#     if row['high'] > prev_close:
#         df.loc[i, 'wo_touched'] = 1