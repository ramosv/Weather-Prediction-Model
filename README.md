# Colorado Climate Forecast

## Overview

The following project is aimed at using historical weather data from the National Center for Environmental Information to predict future temperature trends in the state of Colorado. By analyzing past patterns and changes in temperature, our goal is to provide insights into what the future climate of Colorado may look like, particularly in the context of global warming and environmental changes.

## Notes on the data

Historical weather data came from the [National Center for Environmental Information](https://www.ncdc.noaa.gov/cdo-web/datatools/)

We used Local Climatological Data (LCD), which consist of measurements taken multiple times a day, amounting to over 100,000 entries per year.

#### Missing Data: Denver-2013 and Alamosa-2014

DENVER INTERNATIONAL AIRPORT, CO US (Station ID: WBAN:03017)
We encountered missing data for Denver in 2013 and Alamosa in 2014. For Denver, we used data fromDENVER INTERNATIONAL AIRPORT, CO US (Station ID: WBAN:03017). Despite efforts, the data for 2013 was not available. Similarly, data for ALAMOSA BERGMAN FIELD, CO US (Station ID: WBAN:23061) was missing for 2014.

#### Addressing Missing Data

We used data from adjacent years (2012 and 2014 for Denver, 2013 and 2015 for Alamosa) to predict the missing years. The graphs below show the estimated monthly average temperatures for these missing years.

#### Data Visualization 

##### Missing Denver 2013 and Alamosa 2014
![image](Screenshots/MissingData.png 'Missing Denver 2013 and Alamosa 2014')

Here are the results of estimating what the year 2013 in Denver would look like by taking daily average from 2012 and 2014.

##### Monthly Average Temperatures in Denver (2012-2014)
![image](Screenshots/Denver-2013.png 'Monthly Average Temperatures in Denver (2012-2014)')

Here are the results of estimating what the year 2014 in Alamosa would look like by taking daily average from 2013 and 2015.

##### Monthly Average Temperatures in Alamosa (2013-2015)
![image](Screenshots/Alamosa-2014.png 'Monthly Average Temperatures in Alamosa (2013-2015)')


#### Graphs representing Monthly Temperatures of all 4 locations used in this project. Graphing large data sets is a good way to make sure it is consistent and there are no missing values.

##### Average Monthly Temperature by Location 2003-2012
![image](Screenshots/AVGMonthly(2003-2012).png 'Average Monthly Temperature by Location 2003-2012')


##### Average Monthly Temperature by Location 2013-2022
![image](Screenshots/AVGMonthly(2013-2022).png 'Average Monthly Temperature by Location 2013-2022')


### Fixing Issue "Calculating high and low temperatures from daily averages"
Addressing the latest issue generated some expected problems in missingData.py, preprocessing.py and model.py files.

By closing the issue and addressing the main concern of missing Min and Max values for the mode. A new problem was generated in the initial steps of preprocessing, specifucally regarding missing data from Denver 2013 and Alamosa 2014. I have fix this problem in the latest push. Below is a graph of missing years data with min and max values.

Fixing the issue also rendered some, not all, of the graphing funcions useless. I have commmented them out for now.

##### Monthly Average Temperatures in Denver 2013
![image](Screenshots/Denver-2013-Min-Max.png 'Average Monthly Temperature in Denver 2013')


##### Monthly Average Temperatures in Alamosa 2014
![image](Screenshots/Alamosa-2014-Min-Max.png 'Average Monthly Temperature in Alamosa 2014')


### Final Check for all locations making sure there are no 'Holes' in the data.

##### Denver Monthly Temperature 2003-2022
![image](Screenshots/ALL_Denver.png 'Denver Monthly Temperature 2003-2022')

##### Grand Junction Monthly Temperature 2003-2022
![image](Screenshots/ALL_Grand.png 'Grand Monthly Temperature 2003-2022')

##### Alamosa Monthly Temperature 2003-2022
![image](Screenshots/ALL_Alamosa.png 'Alamosa Monthly Temperature 2003-2022')

##### Colorado Springs Monthly Temperature 2003-2022
![image](Screenshots/ALL_Springs.png 'Springs Monthly Temperature 2003-2022')