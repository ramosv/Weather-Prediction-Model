import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
from pmdarima import auto_arima
import joblib

from preprocessing import preprocessing


#ARIMA (Autoregressive Integrated Moving Average)
"""
A brief description of both models: https://medium.com/@meritshot/introduction-to-arima-and-sarima-for-time-series-forecasting-5af5025c8876
The model library: https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html
"""
def build_model(location):
    all_data = preprocessing()

    location_columns = ['DATE',location]
    location_data = all_data[location_columns]

    location_data['DATE'] = pd.to_datetime(location_data['DATE'])
    location_data.set_index('DATE',inplace=True)

    """Trying resample data to monthly to see if we get a better RMSE and if the model pick up on montlhy sesonal patters
    """
    location_data = location_data.resample('M').mean()

    print(location_data)
    #Splitting between train and test sets
    train_size = int(len(location_data)* 0.8)
    train, test = location_data[0:train_size], location_data[train_size:]

    """https://people.duke.edu/~rnau/411arim.htm

    A nonseasonal ARIMA model is classified as an "ARIMA(p,d,q)" model, where:

    p is the number of autoregressive terms,
    d is the number of nonseasonal differences needed for stationarity, and
    q is the number of lagged forecast errors in the prediction equation. 
    
    """
    #Parameter optimization 
    # m parameter is used for season period. Ideally I would like to select daily since our data is sampled that way. But it is very computational expensive

    sarima_model = auto_arima(train,seasonal=True,m=12,stepwise=True,suppress_warnings=True,error_action="ignore",max_order=None,trace=True)
    
    print(f"Optimal SARIMA model order (p,d,q) {sarima_model.order}")
    print(f"Optimal seasonal order: {sarima_model.seasonal_order}")
    
    #Fitting the sarima model with the above parameters
    model_fit = sarima_model.fit(train)

    # Predicting on the test set
    forecast = model_fit.predict(n_periods=len(test))

    # Evaluate the model
    rmse = sqrt(mean_squared_error(test, forecast))
    print(f'Test RMSE: {rmse}')

    model_fit.plot_diagnostics(figsize=(15, 12))
    plt.show()

    # Return trained model and forecast
    return model_fit, forecast


if __name__ == "__main__":
    model_min, forecast_min = build_model('Grand min')
    model_max, forecast_max = build_model('Grand max')

    # Save the model to be used later (Not needed right now since computation does not take very long with m=12) 
    #localPath = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/"
    #joblib.dump(model_min, localPath+'sarima_modelMax.joblib')
    #joblib.dump(model_max, localPath+'sarima_modelMax.joblib')


