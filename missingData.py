import pandas as pd
import matplotlib.pyplot as plt

path = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/raw_data/Weather Prediction Raw Data/"

# Before preprocessing the last decade we will have to deal with missing data for the year 2013 in Denver and the year 2014 in Alamosa

def process_missing_DenverData2013():
    fillInDenver = 'Denver-2012-2015.csv'

    Denver_2012_2015 = pd.read_csv(path+fillInDenver, usecols=['DATE','HourlyDryBulbTemperature'])
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

    return (Denver_2012,Denver_2013,Denver_2014)


def plottingDenver(prevYear,missingYear,nextYear):
    #Plotting it to make sure 2013 looking half decent

    # Set 'DATE' as the index for each DataFrame
    prevYear.set_index('DATE', inplace=True)
    missingYear.set_index('DATE', inplace=True)
    nextYear.set_index('DATE', inplace=True)

    # Resample and calculate the monthly mean temperature for each DataFrame
    monthly_avg_2012 = prevYear.resample('M')['HourlyDryBulbTemperature'].mean()
    monthly_avg_2013 = missingYear.resample('M')['HourlyDryBulbTemperature'].mean()
    monthly_avg_2014 = nextYear.resample('M')['HourlyDryBulbTemperature'].mean()

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


def process_missing_AlamosaData2014():
    fillInAlamosa = 'Alamosa-2013-2016.csv'

    Alamosa_2013_2016 = pd.read_csv(path+fillInAlamosa, usecols=['DATE','HourlyDryBulbTemperature'])
    Alamosa_2013_2016['DATE'] = pd.to_datetime(Alamosa_2013_2016['DATE'])

    #Adding location column
    Alamosa_2013_2016['Location'] = 'Alamosa'

    #Dropping the year 2016
    Alamosa_2013_2015 = Alamosa_2013_2016[Alamosa_2013_2016['DATE'].dt.year != 2016]

    #Filling in data for missing values
    Alamosa_2013_2015['HourlyDryBulbTemperature'] = pd.to_numeric(Alamosa_2013_2015['HourlyDryBulbTemperature'],errors='coerce')
    Alamosa_2013_2015['HourlyDryBulbTemperature'].interpolate(inplace=True)
    Alamosa_2013_2015['HourlyDryBulbTemperature'].fillna(method='ffill',inplace=True)
    Alamosa_2013_2015['HourlyDryBulbTemperature'].fillna(method='bfill',inplace=True)


    #Separating the years and calculating averages for each hour of each day
    Alamosa_2013 = Alamosa_2013_2015[Alamosa_2013_2015['DATE'].dt.year == 2013]
    avg_daily_2013 = Alamosa_2013.groupby(Alamosa_2013['DATE'].dt.date)['HourlyDryBulbTemperature'].mean()

    #Dropping the leap year so the lengths are the same
    #avg_daily_2013 = avg_daily_2013.drop(pd.Timestamp('2012-02-29'))

    Alamosa_2015 = Alamosa_2013_2015[Alamosa_2013_2015['DATE'].dt.year == 2015] 
    avg_daily_2015 = Alamosa_2015.groupby(Alamosa_2015['DATE'].dt.date)['HourlyDryBulbTemperature'].mean()

    #Resetting indexes to the same year 
    avg_daily_2013.index = avg_daily_2013.index.map(lambda d: d.replace(year = 2014))
    avg_daily_2015.index = avg_daily_2015.index.map(lambda d: d.replace(year = 2014))

    #Creating Alamosa 2014 with average of 2013 and 2015
    avg_daily_2014 = (avg_daily_2013 + avg_daily_2015) / 2

    #Creating 2014 and mapping the the daily average to hourly averages
    Alamosa_2014 = pd.DataFrame({'DATE':pd.date_range(start='2014-01-01', end='2014-12-31', freq='H')})
    Alamosa_2014['tempDate'] = Alamosa_2014['DATE'].dt.date
    Alamosa_2014['HourlyDryBulbTemperature'] = Alamosa_2014['tempDate'].map(avg_daily_2014)
    Alamosa_2014['HourlyDryBulbTemperature'] = pd.to_numeric(Alamosa_2014['HourlyDryBulbTemperature'], errors='coerce')

    Alamosa_2014['Location'] = 'Alamosa'
    Alamosa_2014.drop(columns=['tempDate'], inplace=True)

    return (Alamosa_2013, Alamosa_2014, Alamosa_2015)


def plottingAlamosa(prevYear,missingYear,nextYear):
#Plotting it to make sure 2014 looking half decent

    # Set 'DATE' as the index for each DataFrame
    prevYear.set_index('DATE', inplace=True)
    missingYear.set_index('DATE', inplace=True)
    nextYear.set_index('DATE', inplace=True)

    # Resample and calculate the monthly mean temperature for each DataFrame
    Alamosa_monthly_avg_2013 = prevYear.resample('M')['HourlyDryBulbTemperature'].mean()
    Alamosa_monthly_avg_2014 = missingYear.resample('M')['HourlyDryBulbTemperature'].mean()
    Alamosa_monthly_avg_2015 = nextYear.resample('M')['HourlyDryBulbTemperature'].mean()

    #Plotting the monthly averages
    plt.figure(figsize=(12, 6))
    plt.plot(Alamosa_monthly_avg_2013.index, Alamosa_monthly_avg_2013, label='2013')
    plt.plot(Alamosa_monthly_avg_2014.index, Alamosa_monthly_avg_2014, label='2014')
    plt.plot(Alamosa_monthly_avg_2015.index, Alamosa_monthly_avg_2015, label='2015')

    plt.xlabel('Month')
    plt.ylabel('Average Temperature')
    plt.title('Monthly Average Temperatures in Alamosa (2013-2015)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    denver2012,denver2013,denver2014 = process_missing_DenverData2013()
    plottingDenver(denver2012,denver2013,denver2014)
    alamosa_2013,alamosa_2014,alamosa_2015 = process_missing_AlamosaData2014()
    plottingAlamosa(alamosa_2013,alamosa_2014,alamosa_2015)