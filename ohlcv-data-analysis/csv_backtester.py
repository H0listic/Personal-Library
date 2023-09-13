import os
import time
import pandas as pd


folder_path = '/home/fam/database/Projects/trading/OHLCV_csv'


def csv_to_dataframe(folder_path: str):
    """
    Iterate over a folder and find all the .csv files.
    Turns each ohlcv.csv file into a dataframe.
    :param: folder_path: the parth of the folder that contains the csv files.
    :return: a list of ohlcv converted into dataframes
    """
    dataframes = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and 'OHLCV' in filename:
            df = pd.read_csv(os.path.join(folder_path, filename))
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')
            df['dayofweek'] = df['date'].dt.day_name()
            # Create the new columns
            df['bull three step'] = None
            df['bear three step'] = None
            df['bull IDF'] = None
            df['bear IDF'] = None
            # print(f"File name: {filename}")
            dataframes.append(df)

    return dataframes


def count_weekdays(dataframes):
    """
    Counts the total number of Mondays, Tuesdays, Wednesdays, Thursdays, Fridays, Saturdays, and Sundays in the
    'dayofweek' column of each file
    :param dataframes: a list of dataframes
    """
    for df in dataframes:
        total_mondays = (df['dayofweek'] == 'Monday').sum()
        total_tuesdays = (df['dayofweek'] == 'Tuesday').sum()
        total_wednesdays = (df['dayofweek'] == 'Wednesday').sum()
        total_thursdays = (df['dayofweek'] == 'Thursday').sum()
        total_fridays = (df['dayofweek'] == 'Friday').sum()
        total_saturdays = (df['dayofweek'] == 'Saturday').sum()
        total_sundays = (df['dayofweek'] == 'Sunday').sum()
        print(f"""
        Mondays: {total_mondays},
        Tuesdays: {total_tuesdays},
        Wednesdays: {total_wednesdays},
        Thursdays: {total_thursdays},
        Fridays: {total_fridays},
        Saturdays: {total_saturdays},
        Sundays: {total_sundays}""")


def three_step_pattern(dataframes):
    """
    Locates, counts, calculates profitability of three-step candle patterns on 1D timeframes.
    :param: dataframes: List of OHLC dataframes
    :return: Amount of and profitability of three-step candle pattern on given asset.
    """
    for df_index, df in enumerate(dataframes):

        # Iterate over the rows of the dataframe
        for i in range(len(df) - 3):
            AO = df.loc[i, 'open']
            AC = df.loc[i, 'close']
            BO = df.loc[i + 1, 'open']
            BC = df.loc[i + 1, 'close']
            CO = df.loc[i + 2, 'open']
            CC = df.loc[i + 2, 'close']
            DO = df.loc[i + 3, 'open']
            DC = df.loc[i + 3, 'close']

            # Check for the bullish 4 candle pattern
            if AC > AO and BC < BO and BC > AO and CC < BC and CC > AO and DC > AC:
                df.at[i + 3, 'bull three step'] = 'X'

            # Check for the bearish 4 candle pattern
            if AC < AO and BC > BO and BC < AO and CC > BC and CC < AO and DC < AC:
                df.at[i + 3, 'bear three step'] = 'X'

            # Save the new dataframe to a new csv file
            df.to_csv(f'/home/fam/database/Projects/trading/three_step_{df_index}.csv', index=False)


def inside_day_failure(dataframes):
    for df_index, df in enumerate(dataframes):

        # Iterate over the rows of dataframes
        for i in range(len(df) - 2):
            AH = df.loc[i, 'high']
            AL = df.loc[i, 'low']
            BH = df.loc[i + 1, 'high']
            BO = df.loc[i + 1, 'open']
            BL = df.loc[i + 1, 'low']
            CH = df.loc[i + 2, 'high']
            CC = df.loc[i + 2, 'close']
            CL = df.loc[i + 2, 'low']

            # Check for the bullish inside day failure
            if BH > AH and BL > AL and CL < BL and CH < BH and CC > BO:
                df.at[i + 2, 'bull IDF'] = 'X'

            # Check for the bearish inside day failure
            if BH > AH and BL > AL and CL > BL and CH > BH and CC < BO:
                df.at[i + 2, 'bear IDF'] = 'X'

            # Save the new dataframe to a new csv file
            df.to_csv(f'/home/fam/database/Projects/trading/IDF_{df_index}.csv', index=False)


def engulfing(dataframes):
    # Add a check for volume above MA confluence
    for df_index, df in enumerate(dataframes):
        df['bull engulf'] = ''
        df['bear engulf'] = ''

        # Iterate over the rows in each dataframe
        for i in range(len(df) - 1):
            AO = df.loc[i, 'open']
            AH = df.loc[i, 'high']
            AL = df.loc[i, 'low']
            AC = df.loc[i, 'close']
            BO = df.loc[i, 'open']
            BH = df.loc[i, 'high']
            BL = df.loc[i, 'low']
            BC = df.loc[i, 'close']

            # Check for bullish engulfing pattern
            if AC < AO < BC and BH > AH and BL < AL:
                df.at[i + 1, 'bull engulf'] = 'X'

            # Check for bearish engulfing pattern
            if AC > AO > BC and BH > AH and BL < AL:
                df.at[i + 1, 'bear engulf'] = 'X'

            # Save the new dataframe to a new csv file
            df.to_csv(f'/home/fam/database/Projects/trading/Engulfing_{df_index}.csv', index=False)


def count_totals(dataframes):
    for df in dataframes:
        total_bull_three_step = (df['bull three step'] == 'X').sum()
        total_bear_three_step = (df['bear three step'] == 'X').sum()
        total_bull_idf = (df['bull IDF'] == 'X').sum()
        total_bear_idf = (df['bear IDF'] == 'X').sum()
        print(f"""
        Total bullish three steps: {total_bull_three_step},
        Total bearish three steps: {total_bear_three_step},
        Total bullish idf: {total_bull_idf},
        Total bearish idf: {total_bear_idf}
        """)

# define daily candle patterns to iterate over.

# solve for, how often does price touch LWH, LWL and on what day.

# solve for, if Monday, buy close, target Monday open, min R/R of 2


start_time = time.time()

csv_to_dataframe(folder_path)

# count_weekdays(csv_to_dataframe(folder_path))
#
# three_step_pattern(csv_to_dataframe(folder_path))
#
# inside_day_failure(csv_to_dataframe(folder_path))
#
# count_totals(csv_to_dataframe(folder_path))

engulfing(csv_to_dataframe(folder_path))

end_time = time.time()

print('Elapsed time: ', end_time - start_time)
