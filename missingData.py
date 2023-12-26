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


    #Function to calculate min and max 
    def calculate_daily_min_max(dafr):
        daily = dafr.groupby(dafr['DATE'].dt.date)['HourlyDryBulbTemperature'].agg(['min','max'])
        daily.index = pd.to_datetime(daily.index)
        return daily

    Denver_2012  = calculate_daily_min_max(Denver_2012_2014[Denver_2012_2014['DATE'].dt.year == 2012])
    Denver_2014  = calculate_daily_min_max(Denver_2012_2014[Denver_2012_2014['DATE'].dt.year == 2014])


    #Dropping the leap year so the lengths are the same
    Denver_2012 = Denver_2012.drop(pd.Timestamp('2012-02-29'))

    #Resetting indexes to the same year 
    Denver_2012.index = Denver_2012.index.map(lambda d: d.replace(year = 2013))
    Denver_2014.index = Denver_2014.index.map(lambda d: d.replace(year = 2013))

    #Creating Denver 2013 with average of 2012 and 2014
    Denver_2013 = (Denver_2012 + Denver_2014) / 2
    Denver_2013.reset_index(inplace=True)
    Denver_2013.rename(columns={'index':'DATE','min':'Denver min', 'max': 'Denver max'}, inplace=True)

    #print(Denver_2013)
    '''
                DATE  Denver min  Denver max
    0   2013-01-01        16.0        38.5
    1   2013-01-02        16.5        46.5
    2   2013-01-03        27.5        57.0
    3   2013-01-04        16.0        44.0
    4   2013-01-05        16.0        37.0
    ..         ...         ...         ...
    360 2013-12-27         6.5        26.5
    361 2013-12-28         9.5        34.0
    362 2013-12-29         3.0        23.0
    363 2013-12-30        -1.0        19.5
    364 2013-12-31         2.0        25.0
    '''

    return Denver_2013


# def plottingDenver(prevYear,missingYear,nextYear):
#     #Plotting it to make sure 2013 looking half decent

#     # Set 'DATE' as the index for each DataFrame
#     prevYear.set_index('DATE', inplace=True)
#     missingYear.set_index('DATE', inplace=True)
#     nextYear.set_index('DATE', inplace=True)

#     # Resample and calculate the monthly mean temperature for each DataFrame
#     monthly_avg_2012 = prevYear.resample('M')['HourlyDryBulbTemperature'].mean()
#     monthly_avg_2013 = missingYear.resample('M')['HourlyDryBulbTemperature'].mean()
#     monthly_avg_2014 = nextYear.resample('M')['HourlyDryBulbTemperature'].mean()

#     #Plotting the monthly averages
#     plt.figure(figsize=(12, 6))
#     plt.plot(monthly_avg_2012.index, monthly_avg_2012, label='2012')
#     plt.plot(monthly_avg_2013.index, monthly_avg_2013, label='2013')
#     plt.plot(monthly_avg_2014.index, monthly_avg_2014, label='2014')

#     plt.xlabel('Month')
#     plt.ylabel('Average Temperature')
#     plt.title('Monthly Average Temperatures in Denver (2012-2014)')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


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

    #Function to calculate min and max 
    def calculate_daily_min_max(dafr):
        daily = dafr.groupby(dafr['DATE'].dt.date)['HourlyDryBulbTemperature'].agg(['min','max'])
        daily.index = pd.to_datetime(daily.index)
        return daily


    Alamosa_2013 = calculate_daily_min_max(Alamosa_2013_2015[Alamosa_2013_2015['DATE'].dt.year == 2013])
    Alamosa_2015 = calculate_daily_min_max(Alamosa_2013_2015[Alamosa_2013_2015['DATE'].dt.year == 2015])

    #Resetting indexes to the same year 
    Alamosa_2013.index = Alamosa_2013.index.map(lambda d: d.replace(year = 2014))
    Alamosa_2015.index = Alamosa_2015.index.map(lambda d: d.replace(year = 2014))

    #Creating Alamosa 2014 with average of 2013 and 2015
    Alamosa_2014 = (Alamosa_2013 + Alamosa_2015) / 2
    Alamosa_2014.reset_index(inplace = True)
    Alamosa_2014.rename(columns={'index':'DATE','min':'Alamosa min','max':'Alamosa max'},inplace=True)

    print(Alamosa_2014)
    '''
                DATE  Alamosa min  Alamosa max
    0   2014-01-01        -15.5    21.500000
    1   2014-01-02        -18.5    16.500000
    2   2014-01-03        -19.5    20.000000
    3   2014-01-04        -20.0    21.000000
    4   2014-01-05        -14.5    22.142857
    ..         ...          ...          ...
    360 2014-12-27         -4.5    24.500000
    361 2014-12-28         -5.5    25.000000
    362 2014-12-29         -2.0    27.000000
    363 2014-12-30         -5.0    22.500000
    364 2014-12-31         -7.5    21.000000
    '''


    return Alamosa_2014


# def plottingAlamosa(prevYear,missingYear,nextYear):
# #Plotting it to make sure 2014 looking half decent

#     # Set 'DATE' as the index for each DataFrame
#     prevYear.set_index('DATE', inplace=True)
#     missingYear.set_index('DATE', inplace=True)
#     nextYear.set_index('DATE', inplace=True)

#     # Resample and calculate the monthly mean temperature for each DataFrame
#     Alamosa_monthly_avg_2013 = prevYear.resample('M')['HourlyDryBulbTemperature'].mean()
#     Alamosa_monthly_avg_2014 = missingYear.resample('M')['HourlyDryBulbTemperature'].mean()
#     Alamosa_monthly_avg_2015 = nextYear.resample('M')['HourlyDryBulbTemperature'].mean()

#     #Plotting the monthly averages
#     plt.figure(figsize=(12, 6))
#     plt.plot(Alamosa_monthly_avg_2013.index, Alamosa_monthly_avg_2013, label='2013')
#     plt.plot(Alamosa_monthly_avg_2014.index, Alamosa_monthly_avg_2014, label='2014')
#     plt.plot(Alamosa_monthly_avg_2015.index, Alamosa_monthly_avg_2015, label='2015')

#     plt.xlabel('Month')
#     plt.ylabel('Average Temperature')
#     plt.title('Monthly Average Temperatures in Alamosa (2013-2015)')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


if __name__ == "__main__":
    denver2013 = process_missing_DenverData2013()
    
    #plottingDenver(denver2012,denver2013,denver2014)
    alamosa_2014 = process_missing_AlamosaData2014()
    
    #plottingAlamosa(alamosa_2013,alamosa_2014,alamosa_2015)