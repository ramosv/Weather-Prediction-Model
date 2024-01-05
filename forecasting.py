import pandas as pd
import matplotlib.pyplot as plt

from model import build_model


def forecast_temperature(model,features,data,total_days,location):
    # Predicting future min and max temperatures using model from model.py and data from preprocessing.py
    # After each day predicting we are recalculating the features making a dynamic and iterative forecast

    predictions = []

    for day in range(total_days):
        #iloc looks at the indexed row and returns it as a column: In here we are grabbing the last set of features
        current_features = data[features].iloc[-1].values.reshape(1,-1)

        #predicting tomorrow
        tomorrow = model.predict(current_features)[0]
        predictions.append(tomorrow)

        #update the dataframe
        data = update_features(data,tomorrow,location)


    return predictions

def update_features(data,tomorrow,location):
    # as we continue to predict into the future, we need to update the dataframe with this predictions as well
    new_date = data['DATE'].iloc[-1] + pd.Timedelta(days=1)

    #now row + new predictions
    new_row = pd.DataFrame({'DATE':[new_date], location: [tomorrow]})
    data = pd.concat([data,new_row],ignore_index=True)

    #Feature update
    data[f"{location}_lag_1"] = data[location].shift(1)

    window_sizes = [1,7,14,30]

    for window_size in window_sizes:
        data[f"{location}_rolling_mean_{window_size}"] = data[location].rolling(window=window_size).mean()
        data[f"{location}_rolling_median_{window_size}"] = data[location].rolling(window=window_size).median()
        
        if window_size > 1:
            data[f"{location}_rolling_std_{window_size}"] = data[location].rolling(window=window_size).std()

    data[f"{location}_diff"] = data[location].diff()

    data['day_of_year'] = data['DATE'].dt.day_of_year
    data['Month'] = data['DATE'].dt.month

    data.interpolate(method='linear',inplace=True)  
    data.fillna(method='bfill',inplace=True)
    data.fillna(method='ffill',inplace=True)

    print("New lagged feature:", data[f"{location}_lag_1"].iloc[-1])
    print("New rolling mean:", data[f"{location}_rolling_mean_1"].iloc[-1])

    return data  


if __name__ == "__main__":
    model_min, features_min, dataframe_min = build_model('Grand min')
    model_max, features_max, dataframe_max = build_model('Grand max')

    # Predicting the next 2 years + 1 leap day   
    total_days = 2 * 365 + 1
    
    predictions_min = forecast_temperature(model_min,features_min,dataframe_min,total_days,'Grand min')
    predictions_max = forecast_temperature(model_max, features_max, dataframe_max,total_days,'Grand max')

    print(predictions_min[:10])
    print(predictions_max[:10])


    # forecast_date = pd.date_range(start="2023-01-01", periods = len(predictions_min), freq='D')

    # forecast_df = pd.DataFrame({'DATE':forecast_date,'Grand min': predictions_min,'Grand max': predictions_max})

    # plt.figure(figsize=(12, 6))
    # plt.plot(forecast_df['DATE'], forecast_df['Grand min'], label='Grand min Predictions')
    # plt.plot(forecast_df['DATE'], forecast_df['Grand max'], label='Grand max Predictions')
    # plt.title('Temperature Predictions for the Next Period')
    # plt.xlabel('Date')
    # plt.ylabel('Temperature')
    # plt.legend()
    # plt.grid(True)
    # plt.show()