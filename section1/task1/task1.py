# Task1 Get hourly candle data from CryptoCompare
## 1. Explore CryptoCompare Data API
### Required
#### 1. **Write a function** to download histohour data, parameters:
# fsym: BTC, tsym: USDT, start_time="2017-04-01", end_time="2020-04-01", e='binance'

# import libraries
import requests
import pandas as pd

# write a function to extract API data
def get_hour(fsym, tsym, e):
    end_time = 1585699200
    global df1
    global df3
    df1 = pd.DataFrame()
    for i in range(13):
        dat_param1 = {'fsym': fsym , 'tsym': tsym, 'limit': 2000, 'toTs': end_time, 'e': e}
        resp1 = requests.get('https://min-api.cryptocompare.com/data/v2/histohour', params = dat_param1)
        df2 = pd.DataFrame.from_dict(resp1.json()['Data']['Data'])
        df1 = df1.append(df2, ignore_index=True)
        end_time = end_time - 7200000
    
    dat_param2 = {'fsym': fsym, 'tsym': tsym, 'limit': 304, 'toTs': end_time, 'e': e}
    resp2 = requests.get('https://min-api.cryptocompare.com/data/v2/histohour', params = dat_param2)
    df3 = pd.DataFrame.from_dict(resp2.json()['Data']['Data'])

# call function to download data
get_hour('BTC', 'USDT', 'binance')

# format data using pandas
comb_df = pd.concat([df1, df3])
comb_df.sort_values(by=['time'], inplace=True)
final_df = comb_df.drop_duplicates(subset='time', keep='first', inplace=True)
final_df = comb_df.drop(['conversionType', 'conversionSymbol'], axis=1)
final_df.rename(
    columns={
        "volumefrom": "volume",
        "volumeto": "baseVolume",
        "time": "datetime"
    },
    inplace=True
)

final_df['datetime'] = pd.to_datetime(final_df['datetime'], unit='s')

# export data to csv file
final_df.to_csv(r'D:\quant_intern\caw-quant-training\section1\task1\histohour.csv', index=False)





### Optional

#### 1. Modularize your code


#### 2. Add one more data endpoint

