import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from preprocessing import preprocessing


def build_model(location):
    all_data = preprocessing()

    location_columns = ['DATE', location]
    location_data = all_data[location_columns]

    location_data['DATE'] = pd.to_datetime(location_data['DATE'])
    print(location_data)

    #Adding lag and rolling mean features (Feature engineering to help with the models accuracy)
    lag_featues = pd.DataFrame()
    rolling_mean_feature = pd.DataFrame()
    rolling_median_feature = pd.DataFrame()
    rolling_std_feature = pd.DataFrame()
    differential_feature = pd.DataFrame()

    # Shift() function in pandas creates these shifted or lag features from time series data.
    #Adding a lag of 3 day
    for lag in range(1,4):
        lag_featues[f"{location}_lag_{lag}"] = location_data[location].shift(lag)

    # Trying a few different rolling window sizes
    window_sizes = [1,7,14,30]

    for window_size in window_sizes:
        rolling_mean_feature[f"{location}_rolling_mean_{window_size}"] = location_data[location].rolling(window=window_size).mean()
        rolling_median_feature[f"{location}_rolling_median_{window_size}"] = location_data[location].rolling(window=window_size).median()
        
        # Since it was generting a bunch of nan values
        if window_size > 1:
            rolling_std_feature[f"{location}_rolling_std_{window_size}"] = location_data[location].rolling(window=window_size).std()

    # Differential features
    differential_feature[f"{location}_diff"] = location_data[location].diff()

    # Seasonality features
    location_data['day_of_year'] = location_data['DATE'].dt.dayofyear
    location_data['month'] = location_data['DATE'].dt.month
    location_data['season'] = (location_data['DATE'].dt.month%12 + 3)//3
    

    location_data = pd.concat([location_data,lag_featues,rolling_mean_feature,rolling_median_feature,rolling_std_feature,differential_feature],axis=1)

    print(location_data)

    # Handling missing values from lag and rolling features
    location_data.interpolate(method='linear',inplace=True)  
    location_data.fillna(method='bfill',inplace=True)
    location_data.fillna(method='ffill',inplace=True)

    model= RandomForestRegressor(n_estimators=100, random_state=42)

    #preparing feature matrix X and target vector y
    X = location_data.drop(['DATE', location], axis=1)
    y = location_data[location]

    # Splitting data into training and testing sets (80% train, 20% test)
    # using train_test_split: Split arrays or matrices into random train and test subsets.
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

    # Train from training data
    model.fit(X_train, y_train)

    # Predict on test data
    y_predict = model.predict(X_test)

    # Evaluate the model
    rmse = np.sqrt(mean_squared_error(y_test, y_predict))
    print(f"RMSE: {rmse}")

    #feature importances
    feature_importances = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': feature_importances})
    print(importance_df.sort_values(by='Importance', ascending=False))

    # Return trained model, features used in training and dataframe
    return model,X.columns,location_data

if __name__ == "__main__":
    model_min, features_min, dataframe_min = build_model('Grand min')
    model_max, features_max, dataframe_max = build_model('Grand max')

