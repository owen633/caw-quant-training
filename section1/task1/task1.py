# Task1 Get hourly candle data from CryptoCompare
## 1. Explore CryptoCompare Data API
### Required
#### 1. **Write a function** to download histohour data, parameters:
# fsym: BTC, tsym: USDT, start_time="2017-04-01", end_time="2020-04-01", e='binance'

# import libraries
import requests
import pandas as pd
import time
import dateparser
import pytz

from datetime import datetime


# write a function to convert time
def date_to_seconds(date_str):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    d = dateparser.parse(date_str)
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)
    return int((d - epoch).total_seconds())

# write a function to extract API data
def get_hour(fsym, tsym, e, start_time, end_time):
    output_data = pd.DataFrame()
    limit = 2000
    start_ts = date_to_seconds(start_time)
    end_ts = date_to_seconds(end_time)
    df_rows = (end_ts - start_ts)/3600 + 1

    while len(output_data) < df_rows:
        dat_param = {'fsym': fsym , 'tsym': tsym, 'limit':limit, 'e': e, 'toTs': end_ts}
        resp = requests.get('https://min-api.cryptocompare.com/data/v2/histohour', params = dat_param)
        temp_data = pd.DataFrame.from_dict(resp.json()['Data']['Data'])
        output_data = output_data.append(temp_data, ignore_index=True)
        end_ts = temp_data['time'].iloc[0] - 3600
        hour_remain = (end_ts - start_ts)/3600

        if hour_remain < limit:
            dat_param2 = {'fsym': fsym , 'tsym': tsym, 'limit':hour_remain, 'e': e, 'toTs': end_ts}
            resp2 = requests.get('https://min-api.cryptocompare.com/data/v2/histohour', params = dat_param2)
            final_data = pd.DataFrame.from_dict(resp2.json()['Data']['Data'])
            output_data = output_data.append(final_data, ignore_index=True)
            break

    return output_data
    
# write a function to format data
def format_data(df):
    tidy_df = df.sort_values(by=['time'], inplace=False).rename(
    columns={
        "volumefrom": "volume",
        "volumeto": "baseVolume",
        "time": "datetime"
        }, inplace=False
    ).drop(['conversionType', 'conversionSymbol'], axis=1, inplace=False)
    
    tidy_df['datetime'] = pd.to_datetime(tidy_df['datetime'], unit='s')

    return tidy_df

# execute module code and export to csv file
if __name__ == '__main__':
    raw_data = get_hour('BTC', 'USDT', 'binance', '2017-04-01', '2020-04-01')
    formatted_data = format_data(raw_data)
    formatted_data.to_csv('.\histohour.csv', index=False)






### Optional

#### 1. Modularize your code


#### 2. Add one more data endpoint

