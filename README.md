# Weather-Prediction-Model

Weather Prediction Model for the State of Colorado

---

### Eddie's notes in how I setup my dev environment

#### Unzip data

> `unzip ./Weather\ Prediction\ Raw\ Data.zip -d ./raw_data`

#### Virtual environment

Run the following commands:

> `source .venv/bin/activate` [^1]

> `pip install pip --upgrade`

> `pip install -r ./requirements.txt`

#### Adding jupyter notebooks to vs code

[Read article here](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#:~:text=Jupyter%20Notebooks%20in%20VS%20Code,and%20through%20Python%20code%20files.)

> Note from Eddie: I didn't need to follow the above steps. Once you get the data unzipped, the virtual env. made, and all the packages installed, you should be able to open the `test.ipynb` and VSCode will have a message box pop-up asking to install extensions for Jupyter notebooks.

[^1]: Note this may be different on Windows!


### Notes on the data

#### Historal weather data came from the National Center for Enviromental Information: 
We are missing data from Denver https://www.ncdc.noaa.gov/cdo-web/datatools/

We used Local Climatological Data (LCD) which are station that collect data over time. The data is often taken couple of times every hour. Totally to over 100,000 entries per year.

For Denver we used DIA(Denver International Airport) for some reason they were missing data for the 2013 calendar year. I spent many hours and tried many different approaches to request this data from the site, but for some reason it was not availble. 

To address the missing data. We will gather data from 2012 and 2014 to make a prediction on what the data for 2013 would have looked like.

Here are the results of estimating what the 2013 in Denver year would look like by taking daily average from 2012 and 2014 and creating 2013.


#### Monthly Average Temperatures in Denver (2012-2014)
![image](Screenshots/Figure_2.png 'Monthly Average Temperatures in Denver (2012-2014)')

#### Average Monthly Temperature by Location 2003-2013
![image](Screenshots/Figure_1.png 'Average Monthly Temperature by Location')



