import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from missingData import process_missing_DenverData2013,process_missing_AlamosaData2014

def preprocessing():

    #########  Now dealing with 2003 to 2012 ############
    fileNames = ['Alamosa-2003-2012.csv','Denver-2003-2012.csv','Grand-2003-2012.csv','Springs-2003-2012.csv']
    path = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/raw_data/Weather Prediction Raw Data/"
    allFrames = []

    for file in fileNames:
        temp_frame = pd.read_csv(os.path.join(path,file),usecols=["DATE","HourlyDryBulbTemperature"])
        temp_frame["DATE"] = pd.to_datetime(temp_frame["DATE"])

        temp_frame['HourlyDryBulbTemperature'] = pd.to_numeric(temp_frame['HourlyDryBulbTemperature'],errors='coerce')
        temp_frame["HourlyDryBulbTemperature"].interpolate(inplace=True)
        temp_frame["HourlyDryBulbTemperature"].fillna(method='ffill',inplace=True)
        temp_frame["HourlyDryBulbTemperature"].fillna(method='bfill',inplace=True)

        location = file.split('-')[0]
        temp_frame["Location"] = location    
        allFrames.append(temp_frame)

    # Combine the data into a single data frame sorted by date
    combined_frames = pd.concat(allFrames, ignore_index=True)
    combined_frames.sort_values(by='DATE',inplace=True)

    # Group my month and location and get average
    combined_frames['Month'] = combined_frames['DATE'].dt.to_period('M')
    monthlyAverage = combined_frames.groupby(['Month','Location']).agg(AvgTemp =('HourlyDryBulbTemperature', 'mean')).reset_index()
    monthlyAverage['Month'] = monthlyAverage['Month'].dt.to_timestamp()

    #Pivot the dataframe. For locations as columns and months as rows
    pivot1 = monthlyAverage.pivot(index='Month',columns='Location',values='AvgTemp')

    #graphing_data(pivot1)

    #########  Now dealing with 2013 to 2022 ############
    morefiles = ['Alamosa-2013-2022.csv','Denver-2014-2022.csv','Grand-2013-2022.csv','Springs-2013-2022.csv']
    frames = []

    for file in morefiles:
        temp_frame = pd.read_csv(os.path.join(path,file),usecols=['DATE','HourlyDryBulbTemperature'])

        temp_frame['DATE'] = pd.to_datetime(temp_frame['DATE'])
        temp_frame['HourlyDryBulbTemperature'] = pd.to_numeric(temp_frame['HourlyDryBulbTemperature'],errors='coerce')
        temp_frame['HourlyDryBulbTemperature'].interpolate(inplace=True)
        temp_frame['HourlyDryBulbTemperature'].fillna(method='ffill',inplace=True)
        temp_frame['HourlyDryBulbTemperature'].fillna(method='bfill',inplace=True)

        location = file.split('-')[0]
        temp_frame['Location'] = location
        frames.append(temp_frame)

    #Missing year for Denver(2013)
    denver2012,denver2013,denver2014 = process_missing_DenverData2013()
    frames.append(denver2013)

    #Missing year for Alamosa(2014)
    alamosa2013,alamosa2014,alamosa2015 = process_missing_AlamosaData2014()
    frames.append(alamosa2014)

    # Combine the data into a single data frame sorted by date
    combFrames = pd.concat(frames,ignore_index=True)
    combFrames.sort_values(by='DATE', inplace=True)

    # Group my month and location and get average: For graphing function
    combFrames['Month'] = combFrames['DATE'].dt.to_period('M')
    monthlyAvg = combFrames.groupby(['Month','Location']).agg(AvgTemp = ('HourlyDryBulbTemperature','mean')).reset_index()
    monthlyAvg['Month'] = monthlyAvg['Month'].dt.to_timestamp()

    #Pivot the dataframe. For locations as columns and months as rows
    pivot2 = monthlyAvg.pivot(index='Month',columns='Location',values='AvgTemp')

    #graphing_data(pivot2)

    # Combine the two dataframes (20 years of data) and sort
    all_data = pd.concat([combined_frames,combFrames], ignore_index=True)
    all_data.sort_values(by='DATE',inplace=True)

    #print(all_data)
    '''
                            DATE  HourlyDryBulbTemperature Location    Month
    0      2003-01-01 00:00:00                      18.0  Alamosa  2003-01
    1      2003-01-01 00:00:00                      29.0    Grand  2003-01
    2      2003-01-01 00:00:00                      31.0  Springs  2003-01
    3      2003-01-01 00:02:00                      32.0   Denver  2003-01
    4      2003-01-01 00:52:00                      18.0  Alamosa  2003-01
    ...                    ...                       ...      ...      ...
    992823 2022-12-31 23:59:00                      36.0  Alamosa  2022-12
    992818 2022-12-31 23:59:00                      36.0  Alamosa  2022-12
    992817 2022-12-31 23:59:00                      40.0  Springs  2022-12
    992819 2022-12-31 23:59:00                      39.0    Grand  2022-12
    992824 2022-12-31 23:59:00                      28.0   Denver  2022-12
    '''

    # Dealing with issue "Calculating high and low temperatures from daily averages"
    # the .agg() method allows the application of multiple operands and functions
    
    # Turning into daily averages: First lets take the date without the time and place into a new column
    all_data['DATE'] = pd.to_datetime(all_data['DATE'])
    all_data['DATE_ONLY'] = all_data['DATE'].dt.date

    #Grouping data by DATE_ONLY and Location
    daily_stats = all_data.groupby(['DATE_ONLY','Location'])['HourlyDryBulbTemperature'].agg(['max','min']).reset_index()

    # pivoting the data so that each locations temp is a separate column: Pivot functions returns a 'reshapes' dataframe
    daily_stats_pivot = daily_stats.pivot(index='DATE_ONLY',columns='Location').reset_index()

    #Renaming back to date
    daily_stats_pivot.rename(columns={'DATE_ONLY':'DATE'}, inplace=True)

    """
                DATE_ONLY     max         ...    min
    Location             Alamosa Denver  ... Denver Grand    Springs
    0         2003-01-01    39.0   43.0  ...   25.5  23.0  23.666667
    1         2003-01-02    38.0   54.0  ...   24.0  19.0  18.000000
    2         2003-01-03    44.0   60.0  ...   35.0  18.0  31.666667
    3         2003-01-04    50.0   54.0  ...   31.0  20.0  29.000000
    4         2003-01-05    45.0   50.0  ...   35.0  23.0  29.000000
    """

    # Using agg with groupy here generated a multi-level header that looks like ('Alamosa, 'min') and (Alamosa, 'max')
    # We will be flattening this by concatenating the strings to 'Alamosa min'and 'Alamosa max' 

    flattened_names= []
    for col in daily_stats_pivot.columns:
        #Skip DATE
        if col[0] == 'DATE':
            flattened_names.append('DATE')
        else:
            #Combining the multilevel columns names
            joined = ' '.join(col).strip()

            #Making the location name come before the min or max
            if joined.startswith('max') or joined.startswith('min'):
                parts = joined.split(' ')
                new = f"{parts[1]} {parts[0]}"
                flattened_names.append(new)
            else:
                flattened_names.append(col)
    
    #Updates the names
    daily_stats_pivot.columns = flattened_names


    #print(daily_stats_pivot)
    '''
                DATE  Alamosa max  Denver max  Grand max  Springs max  Alamosa min  Denver min  Grand min  Springs min
    0     2003-01-01         39.0        43.0       29.0         37.0    11.333333        25.5       23.0    23.666667
    1     2003-01-02         38.0        54.0       39.0         49.0     2.000000        24.0       19.0    18.000000
    2     2003-01-03         44.0        60.0       42.0         56.0     6.000000        35.0       18.0    31.666667
    3     2003-01-04         50.0        54.0       44.0         46.0    10.000000        31.0       20.0    29.000000
    4     2003-01-05         45.0        50.0       40.0         47.0    13.000000        35.0       23.0    29.000000
    ...          ...          ...         ...        ...          ...          ...         ...        ...          ...
    7300  2022-12-27         47.0        61.0       35.0         63.0     5.000000        37.0       23.0    33.000000
    7301  2022-12-28         47.0        50.0       36.0         50.0    23.000000        29.0       30.5    33.000000
    7302  2022-12-29         36.0        31.0       30.0         35.0     8.000000        17.0       16.0    15.500000
    7303  2022-12-30         37.0        37.0       33.0         37.0     6.000000        18.0       22.0    15.000000
    7304  2022-12-31         49.0        46.0       39.0         57.0     6.000000        28.0       28.0    28.000000
    '''
    # Writting data to file
    # localPath = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/"
    # daily_stats_pivot.to_csv(localPath+"Combined_Data")

    return daily_stats_pivot

def graphing_data(data_frame):
     
    plt.figure(figsize=(12,6))

    for location in data_frame.columns:
        plt.plot(data_frame.index, data_frame[location], marker='',label=location)

    plt.xlabel('Month')
    plt.ylabel('Average Temperature')
    plt.title('Average Monthly Temperature by Location')
    plt.legend(title='Location')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    preprocessing()