import os
import numpy as np
import pandas as pd


folder_path = '/home/fam/database/Projects/trading/OHLCV_csv'


def get_ohlcv_dataframes(folder_path: str):
    dataframes = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and "OHLC" in filename:
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')
            df['dayofweek'] = df['date'].dt.day_name()
            dataframes.append(df)
    return dataframes


def count_days_of_week(dataframes):
    day_counts = []
    for df in dataframes:
        days = np.unique(df['dayofweek'])
        day_count = {day: len(df[df['dayofweek'] == day]) for day in days}
        day_counts.append(day_count)
    return day_counts


dataframes = get_ohlcv_dataframes(folder_path)
day_counts = count_days_of_week(dataframes)

print(dataframes)

print(day_counts)


def calculate_crosses(dataframes):
    cross_counts = []
    for df in dataframes:
        cross_count = 0
        for i in range(len(df) - 1):
            if df.iloc[i]['dayofweek'] == 'Monday' and df.iloc[i+1]['dayofweek'] == 'Tuesday':
                if df.iloc[i]['close'] > df.iloc[i]['open']:
                    if df.iloc[i+1]['low'] < df.iloc[i]['open']:
                        cross_count += 1
                else:
                    if df.iloc[i+1]['high'] > df.iloc[i]['open']:
                        cross_count += 1
        cross_counts.append(cross_count)
    return cross_counts


crosscounts = calculate_crosses(dataframes)

print(crosscounts)
# solve for, if buy monday close and target monday open
    # calculate average R
    # if bear candle, long, stop at low
    # if bull candle, short, stop at high
    # starting capital = 1k
    # risk = 10% per trade

# solve for monday high of week, tuesday high of week.... sunday high of week.
# solve for above but lows of week
# solve for how often tuesday touches mondays open high low close
# solve for above for every day of week for prior day
# solve for how often price touches weekly open and on what day
# Create empty lists to store data
# tuesday_touches_monday_open = []
# tuesday_higher_than_monday = []
# tuesday_lower_than_monday = []
# friday_lower_than_monday = []
# friday_higher_than_monday = []
# wednesday_high_higher_than_monday_low = []
# wednesday_close_higher_than_monday_close = []
#
# # Iterate over the 'df' dataframe solving for the lists
for i in range(len(df)):
    if df['dayofweek'][i] == 'Tuesday' and df['high'][i] > df['open'][i - 1]:
        tuesday_touches_monday_open.append(df['date'][i])

for i in range(len(df)):
    if df['dayofweek'][i] == 'Tuesday' and df['high'][i] > df['high'][i - 1]:
        tuesday_higher_than_monday.append(df['date'][i])
    else:
        pass

for i in range(len(df)):
    if df['dayofweek'][i] == 'Tuesday' and df['low'][i] < df['low'][i - 1]:
        tuesday_lower_than_monday.append(df['date'][i])
    else:
        pass

for i in range(len(df)):
    if df['dayofweek'][i] == 'Friday' and i >= 4 and df['low'][i] < df.loc[i - 4, 'low']:
        friday_lower_than_monday.append(df['date'][i])
    else:
        pass

for i in range(len(df)):
    if df['dayofweek'][i] == 'Friday' and i >= 4 and df['high'][i] < df.loc[i - 4, 'high']:
        friday_higher_than_monday.append(df['date'][i])
    else:
        pass

# add condition to check if the index is = 1, then pass and look for the next wednesday
for i in range(len(df)):
    # Check if the 'dayofweek' column is equal to Wednesday and the index number is equal to 1
    if df.at[1, 'dayofweek'] == 'Wednesday':
        # Skip ahead 7 rows
        df = df.iloc[7:]
        # Do something here
    if df['dayofweek'][i] == 'Wednesday' and df['high'][i] > df['low'][i - 2]:
        wednesday_high_higher_than_monday_low.append(df['date'][i])

for i in range(len(df)):
    # Check if the 'dayofweek' column is equal to Wednesday and the index number is equal to 1
    if df.at[1, 'dayofweek'] == 'Wednesday':
        # Skip ahead 7 rows
        df = df.iloc[7:]
    if df['dayofweek'][i] == 'Wednesday' and df['close'][i] > df['close'][i - 2]:
        wednesday_close_higher_than_monday_close.append(df['date'][i])


print('There are ', sum(df['Engulfing']), 'engulfing candles')
for i in range(len(df)):
    for day in df['dayofweek']:
        if df['Engulfing'] == 1 and df['dayofweek'] == 'Monday':
            emon.append(df['date'])
print(len(emon))

print(total_mondays, 'Mondays,',
      len(tuesday_touches_monday_open),
      'Tuesdays touch Mondays open:',
      format((len(tuesday_touches_monday_open) / total_mondays) * 100, '.2f'), '% of the time.')

print(total_mondays, 'Mondays,',
      len(tuesday_higher_than_monday),
      'Tuesdays with a higher high than Mondays:',
      format((len(tuesday_higher_than_monday) / total_mondays) * 100, '.2f'), '% of the time.')

print(total_mondays, 'Mondays,',
      len(tuesday_lower_than_monday),
      'Tuesdays with a lower low than Mondays:',
      format((len(tuesday_lower_than_monday) / total_mondays) * 100, '.2f'), '% of the time.')

print(total_mondays, 'Mondays,',
      len(friday_lower_than_monday),
      'Fridays with a lower low than Mondays:',
      format((len(friday_lower_than_monday) / total_mondays) * 100, '.2f'), '% of the time.')

print(total_mondays, 'Mondays,',
      len(friday_higher_than_monday),
      'Fridays with a higher high than Mondays:',
      format((len(friday_higher_than_monday) / total_mondays) * 100, '.2f'), '% of the time.')

print(total_mondays, 'Mondays,',
      len(wednesday_high_higher_than_monday_low),
      'Wednesdays with a higher high than Mondays low:',
      format((len(wednesday_high_higher_than_monday_low) / total_mondays) * 100, '.2f'), '% of the time.')

print(total_mondays, 'Mondays,',
      len(wednesday_close_higher_than_monday_close),
      'Wednesdays with a close than Mondays close:',
      format((len(wednesday_close_higher_than_monday_close) / total_mondays) * 100, '.2f'), '% of the time.')
