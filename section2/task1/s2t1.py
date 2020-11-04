# Task1 Backtest Framework Intro

## Required

### 1. Create a Seperate Repo and Virtual Environment


### 2. Read the Doc and Example


### 3. Write a Hello World Strategy

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  
import os.path  
import sys  
import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:

            if self.dataclose[0] < self.dataclose[-1]:

                    if self.dataclose[-1] < self.dataclose[-2]:
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])
                        self.order = self.buy()

        else:
            
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


# execute strategy and create plot
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './data/nvda-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2014, 1, 1),
        todate=datetime.datetime(2014, 12, 31),
        reverse=False)

    cerebro.adddata(data)

    cerebro.broker.setcash(5000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    figure = cerebro.plot()[0][0]
    figure.savefig('hello_world.png')