# Task2 Get market data from Binance

### Required

#### 1. **Use Binance Python SDK** to get public data

# import libraries
import time
import dateparser
import pytz
import json
import pandas as pd

from datetime import datetime
from binance.client import Client

# write functions to convert time and inverval
def date_to_milliseconds(date_str):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    d = dateparser.parse(date_str)
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    return int((d - epoch).total_seconds() * 1000.0)

def interval_to_milliseconds(interval):
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms

# write function to get candle/klines data
def get_historical_klines(symbol, interval, start_str, end_str=None):
    client = Client("", "")
    output_data = []
    limit = 500
    timeframe = interval_to_milliseconds(interval)
    start_ts = date_to_milliseconds(start_str)
    end_ts = None
    
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    symbol_existed = False
    
    while True:
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            output_data = output_data + temp_data
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        
        else:
            start_ts = start_ts + timeframe

        idx = idx + 1
       
        if len(temp_data) < limit:
            
            break

        if idx % 3 == 0:
            time.sleep(1)

    return output_data

# write function to format candle/klines data
def format_klines(df):
    formatted_klines = pd.DataFrame(df, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                                                'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 
                                                'Taker buy quote asset volume', 'Ignore'], index=None)

    formatted_klines = formatted_klines.drop(['Ignore'], axis=1)
    formatted_klines['Open time'] = pd.to_datetime(formatted_klines['Open time'], unit='ms')
    formatted_klines['Close time'] = pd.to_datetime(formatted_klines['Close time'], unit='ms')

    return formatted_klines


# write function to get transaction/trade data
def get_aggr_trades(symbol, start_str, end_str, fromID = None):
    client = Client("", "")
    output_data = []
    limit = 500
    start_ts = date_to_milliseconds(start_str)
    end_ts = date_to_milliseconds(end_str)

    from_id = None
    
    if fromID:
        from_id = fromID
    
    idx = 0
    symbol_existed = False
    
    while True:
        temp_data = client.get_aggregate_trades(
        symbol=symbol,
        fromId = from_id,
        limit=limit,
        startTime=start_ts,
        endTime=end_ts
        )
        
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            output_data += temp_data
            from_id = str(int(temp_data[-1]['a'] + 1))
            start_ts = None
            end_ts = None

        idx += 1
        
        if temp_data[-1]['T'] >  date_to_milliseconds(end_str):
            temp_data = [i for i in temp_data if not (i['T'] > date_to_milliseconds(end_str))]
            output_data += temp_data
          
            break

        if idx % 3 == 0:
            time.sleep(1)
    
    return output_data



# write function to format transaction/trade data
def format_trades(df):
    formatted_trades = pd.DataFrame.from_dict(df)
    formatted_trades.rename(
    columns={
        "a": "Aggregate tradeId",
        "p": "Price",
        "q": "Quantity",
        "f": "First tradeId",
        "l": "Last tradeId",
        "T": "Timestamp",
        "m": "Was the buyer the maker?",
        "M": "Was the trade the best price match?"

    },
    inplace=True
)

    formatted_trades['Timestamp'] = pd.to_datetime(formatted_trades['Timestamp'], unit='ms')

    return formatted_trades


# write function to get market depth/orderbook data
def get_orderbook(symbol):
    client = Client("", "")
    limit = 1000

    output_data = client.get_order_book(
        symbol=symbol,
        limit=limit,
        )

    return output_data


# write function to format orderbook data
def format_orderbook(df):
    formatted_order = pd.DataFrame.from_dict(df)
    bid = pd.DataFrame(formatted_order['bids'].to_list(), columns=
['Bid Price', 'Bid Quantity'])
    ask = pd.DataFrame(formatted_order['asks'].to_list(), columns=
['Ask Price', 'Ask Quantity'])
    join_order = pd.concat([bid, ask], axis=1)

    return join_order


# execute module code and export to csv file
if __name__ == '__main__':
    raw_data1 = get_historical_klines('BNBBTC', Client.KLINE_INTERVAL_1HOUR, '2019-01-01', '2020-01-01')
    formatted_data1 = format_klines(raw_data1)
    formatted_data1.to_csv('./klines.csv', index=False)


    raw_data2 = get_aggr_trades("ETHBTC", "10 hours ago", "9 hours and 10 minutes ago")
    formatted_data2 = format_trades(raw_data2)
    formatted_data2.to_csv('./trades.csv', index=False)

    raw_data3 = get_orderbook("BNBBTC")
    formatted_data3 = format_orderbook(raw_data3)
    formatted_data3.to_csv('./orderbook.csv', index=False)

    



### Optional, 


#### 1. Trade in Binance by its python SDK
