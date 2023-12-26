import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from preprocessing import preprocessing


def build_model():
    all_data = preprocessing()

    #print(all_data)
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

    all_data['DATE'] = pd.to_datetime(all_data['DATE'])

    #Adding lag and rolling mean features (Feature engineering to help with the models accuracy)
    lag_featues = pd.DataFrame()
    rolling_mean_feature = pd.DataFrame()
    rolling_median_feature = pd.DataFrame()
    rolling_std_feature = pd.DataFrame()
    differential_feature = pd.DataFrame()

    # Shift() function in pandas creates these shifted or lag features from time series data.
    # Adding a lag of 1 day
    for lag in range(1,2):
        for location in ['Alamosa','Grand','Springs','Denver']:
            lag_featues[f"{location}_lag_{lag}"] = all_data[location].shift(lag)

    # Trying a few different rolling window sizes
    window_sizes = [1,3,5,7]

    for window_size in window_sizes:
        for location in ['Alamosa','Grand','Springs','Denver']:
            rolling_mean_feature[f"{location}_rolling_mean_{window_size}"] = all_data[location].rolling(window=window_size).mean()
            rolling_std_feature[f"{location}_rolling_std_{window_size}"] = all_data[location].rolling(window=window_size).std()
            rolling_median_feature[f"{location}_rolling_median_{window_size}"] = all_data[location].rolling(window=window_size).median()

    # Differential features
    for location in ['Alamosa','Grand','Springs','Denver']:
        differential_feature[f"{location}_diff"] = all_data[location].diff()

    # Seasonality features
    all_data['day_of_year'] = all_data['DATE'].dt.dayofyear
    all_data['month'] = all_data['DATE'].dt.month

    all_data = pd.concat([all_data,lag_featues,rolling_mean_feature,rolling_median_feature,rolling_std_feature,differential_feature],axis=1)

    # print(all_data)
    '''
            DATE    Alamosa     Denver  ...  Grand_diff  Springs_diff  Denver_diff
    0    2003-01-01  24.985507  33.523256  ...         NaN           NaN          NaN
    1    2003-01-02  15.527778  37.068966  ...    0.743245     -0.083118     3.545710
    2    2003-01-03  22.891156  47.344828  ...    1.414966     12.130359    10.275862
    3    2003-01-04  26.864583  39.812500  ...    2.224490     -5.221088    -7.532328
    4    2003-01-05  30.284722  41.914286  ...    1.248699      1.367551     2.101786
    ...         ...        ...        ...  ...         ...           ...          ...
    7300 2022-12-27  31.413793  48.848485  ...   -1.017241     16.303571    12.385985
    7301 2022-12-28  36.068966  39.130435  ...    1.466292     -8.203571    -9.718050
    7302 2022-12-29  21.800000  25.578947  ...   -7.973539    -12.451351   -13.551487
    7303 2022-12-30  20.327586  26.424242  ...    4.146135     -0.683131     0.845295
    7304 2022-12-31  30.800000  32.794118  ...    3.043651     16.373192     6.369875
    '''

    # Handling missing values from lag and rolling features
    all_data.interpolate(method='linear',inplace=True)  
    all_data.fillna(method='bfill',inplace=True)
    all_data.fillna(method='ffill',inplace=True)

    print("NaNs after processing:")
    nan_counts = all_data.isna().sum()
    print(type(nan_counts))
    print(f"nan_counts length: {len(nan_counts)}")

    #Store dropped nan
    localPath = "C:/Users/ramosv/Desktop/GitHub/Weather-Prediction-Model/"
    nan_counts.to_csv(os.path.join(localPath,"nanCounts.txt"))


    # Handling persistent NaNs
    if len(nan_counts) > 0:
        # drop columns with NaNs
        all_data.dropna(axis=1, how='all', inplace=True)
        # drop rows with NaNs
        all_data.dropna(axis=0, how='any', inplace=True)


    model= RandomForestRegressor(n_estimators=100, random_state=42)

    X = all_data.drop(['DATE', 'Grand'], axis=1)
    y = all_data['Grand']

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


if __name__ == "__main__":
    build_model()