import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

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



#Combine the data into a single data frame sorted by date
combined_frames = pd.concat(allFrames, ignore_index=True)
combined_frames.sort_values(by='DATE',inplace=True)

#Writting data to file
#localPath = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/"
#combined_frames.to_csv(localPath+"Combined_Data")

#Adding a new month column
combined_frames['Month'] = combined_frames['DATE'].dt.to_period('M')
print(combined_frames)

#Group my month and location and get average
monthlyAverage = combined_frames.groupby(['Month','Location']).agg(AvgTemp =('HourlyDryBulbTemperature', 'mean')).reset_index()
monthlyAverage['Month'] = monthlyAverage['Month'].dt.to_timestamp()
print(monthlyAverage)

#Pivot the dataframe. For locations as columns and months as rows
pivot_df = monthlyAverage.pivot(index='Month',columns='Location',values='AvgTemp')

plt.figure(figsize=(12,6))

for location in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[location], marker='',label=location)

plt.xlabel('Month')
plt.ylabel('Average Temperature')
plt.title('Average Monthly Temperature by Location')
plt.legend(title='Location')
plt.grid(True)
plt.show()


#########  Now dealing with 2013 to 2022 ############
## Before preprossing the last decade we will have to deal with missing data for 2013
## I will be taking hour average from 2012 and 2014 to fill in the data of 2013

fillInData = 'Denver-2012-2015.csv'

Denver_2012_2015 = pd.read_csv(path+fillInData, usecols=['DATE','HourlyDryBulbTemperature'])
Denver_2012_2015['DATE'] = pd.to_datetime(Denver_2012_2015['DATE'])

#Adding location column
Denver_2012_2015['Location'] = 'Denver'

#Dropping the year 2015
Denver_2012_2014 = Denver_2012_2015[Denver_2012_2015['DATE'].dt.year != 2015]

#Filling in data for missing values
Denver_2012_2014['HourlyDryBulbTemperature'] = pd.to_numeric(Denver_2012_2014['HourlyDryBulbTemperature'],errors='coerce')
Denver_2012_2014['HourlyDryBulbTemperature'].interpolate(inplace=True)
Denver_2012_2014['HourlyDryBulbTemperature'].fillna(method='ffill',inplace=True)
Denver_2012_2014['HourlyDryBulbTemperature'].fillna(method='bfill',inplace=True)


#Separating the years and calculating averages for each hour of each day
Denver_2012 = Denver_2012_2014[Denver_2012_2014['DATE'].dt.year == 2012]
avg_daily_2012 = Denver_2012.groupby(Denver_2012['DATE'].dt.date)['HourlyDryBulbTemperature'].mean()

#Dropping the leap year so the lengths are the same
avg_daily_2012 = avg_daily_2012.drop(pd.Timestamp('2012-02-29'))

Denver_2014 = Denver_2012_2014[Denver_2012_2014['DATE'].dt.year == 2014] 
avg_daily_2014 = Denver_2014.groupby(Denver_2014['DATE'].dt.date)['HourlyDryBulbTemperature'].mean()

#Resetting indexes to the same year 
avg_daily_2012.index = avg_daily_2012.index.map(lambda d: d.replace(year = 2013))
avg_daily_2014.index = avg_daily_2014.index.map(lambda d: d.replace(year = 2013))

#Creating Denver 2013 with average of 2012 and 2014
avg_daily_2013 = (avg_daily_2012 + avg_daily_2014) / 2

#Creating 2013 and mapping the the daily average to hourly averages
Denver_2013 = pd.DataFrame({'DATE':pd.date_range(start='2013-01-01', end='2013-12-31', freq='H')})
Denver_2013['tempDate'] = Denver_2013['DATE'].dt.date
Denver_2013['HourlyDryBulbTemperature'] = Denver_2013['tempDate'].map(avg_daily_2013)
Denver_2013['HourlyDryBulbTemperature'] = pd.to_numeric(Denver_2013['HourlyDryBulbTemperature'], errors='coerce')

Denver_2013['Location'] = 'Denver'
Denver_2013.drop(columns=['tempDate'], inplace=True)

#Plotting it to make sure 2013 looking half decent

# Set 'DATE' as the index for each DataFrame
Denver_2012.set_index('DATE', inplace=True)
Denver_2013.set_index('DATE', inplace=True)
Denver_2014.set_index('DATE', inplace=True)

# Resample and calculate the monthly mean temperature for each DataFrame
monthly_avg_2012 = Denver_2012.resample('M')['HourlyDryBulbTemperature'].mean()
monthly_avg_2013 = Denver_2013.resample('M')['HourlyDryBulbTemperature'].mean()
monthly_avg_2014 = Denver_2014.resample('M')['HourlyDryBulbTemperature'].mean()

#Plotting the monthly averages
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg_2012.index, monthly_avg_2012, label='2012')
plt.plot(monthly_avg_2013.index, monthly_avg_2013, label='2013')
plt.plot(monthly_avg_2014.index, monthly_avg_2014, label='2014')

plt.xlabel('Month')
plt.ylabel('Average Temperature')
plt.title('Monthly Average Temperatures in Denver (2012-2014)')
plt.legend()
plt.grid(True)
plt.show()
