import pandas as pd
import matplotlib.pyplot as plt
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