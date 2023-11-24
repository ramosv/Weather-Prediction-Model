import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from missingData import process_missing_DenverData2013,process_missing_AlamosaData2014

def preprocessing():

    #########  Now dealing with 2003 to 2012 ############
    fileNames = ['Alamosa-2003-2012.csv','Denver-2003-2012.csv','Grand-2003-2012.csv','Springs-2003-2012.csv']
    path = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/raw_data/Weather Prediction Raw Data/"
    allFrames = []

    for file in fileNames:
        #os.path.join(path,file)...
        temp_frame = pd.read_csv(path+file,usecols=["DATE","HourlyDryBulbTemperature"])
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

    graphing_data(pivot1)

    #########  Now dealing with 2013 to 2022 ############
    morefiles = ['Alamosa-2013-2022.csv','Denver-2014-2022.csv','Grand-2013-2022.csv','Springs-2013-2022.csv']
    frames = []

    for file in morefiles:
        temp_frame = pd.read_csv(path+file,usecols=['DATE','HourlyDryBulbTemperature'])

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

    graphing_data(pivot2)

    # Combine the two dataframes (20 years of data) and sort
    all_data = pd.concat([combined_frames,combFrames], ignore_index=True)
    all_data.sort_values(by='DATE',inplace=True)

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

    # We can now start preprocessing data for the machine learning model: RandomForestRegressor
    
    # Turning into daily averages: First lets take the date without the time and place into a new column
    all_data['DATE'] = pd.to_datetime(all_data['DATE'])
    all_data['DATE_ONLY'] = all_data['DATE'].dt.date

    #Grouping data by DATE_ONLY and Location
    daily_averages = all_data.groupby(['DATE_ONLY','Location'])['HourlyDryBulbTemperature'].mean().reset_index()

    # pivoting the data so that each locations temp is a separate column: Pivot functions returns a 'reshapes' dataframe
    daily_averages_pivot = daily_averages.pivot(index='DATE_ONLY',columns='Location', values='HourlyDryBulbTemperature').reset_index()

    #Renaming back to date
    daily_averages_pivot.rename(columns={'DATE_ONLY':'DATE'}, inplace=True)

    #Reset index and sort
    daily_averages_pivot.reset_index(drop=True,inplace=True)
    daily_averages_pivot.sort_values(by='DATE',inplace=True)

    #print(daily_averages_pivot)
    '''
    Location        DATE    Alamosa     Denver      Grand    Springs
    0         2003-01-01  24.985507  33.523256  26.692130  31.296296
    1         2003-01-02  15.527778  37.068966  27.435374  31.213178
    2         2003-01-03  22.891156  47.344828  28.850340  43.343537
    3         2003-01-04  26.864583  39.812500  31.074830  38.122449
    4         2003-01-05  30.284722  41.914286  32.323529  39.490000
    ...              ...        ...        ...        ...        ...
    7300      2022-12-27  31.413793  48.848485  31.000000  49.303571
    7301      2022-12-28  36.068966  39.130435  32.466292  41.100000
    7302      2022-12-29  21.800000  25.578947  24.492754  28.648649
    7303      2022-12-30  20.327586  26.424242  28.638889  27.965517
    7304      2022-12-31  30.800000  32.794118  31.682540  44.338710
    '''
    # Writting data to file
    # localPath = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/"
    # daily_averages_pivot.to_csv(localPath+"Combined_Data")

    return daily_averages_pivot

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