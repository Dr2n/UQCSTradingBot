import talib
import pandas as pd


class Strategy():
    def __init__(self, client, timeframe='5m'):
        self.client = client
        self.timeframe = timeframe
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.volume = 0
        self.timestamp = None

    def predict(self):
        ohlcv_candles = pd.DataFrame(self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe,
            symbol='XBTUSD',
            count=100,
            reverse=True
        ).result()[0])

        ohlcv_candles_BXBT = pd.DataFrame(self.client.Trade.Trade_getBucketed(
            binSize=self.timeframe,
            symbol='.BXBT',
            count=100,
            reverse=True
        ).result()[0])
        row = ohlcv_candles.iloc[0]

        self.open = row["open"]
        self.close = row["close"]
        self.high = row["high"]
        self.low = row["low"]
        self.volume = row["foreignNotional"]
        self.timestamp = str(row["timestamp"]).split(':')[0] + ":" + \
                        str(row["timestamp"]).split(':')[1] + ":00"

        ## Print market data
        
        print(f'{self.timestamp} OPEN: {self.open} HIGH: {self.high} LOW: {self.low} CLOSE: {self.close}')

        ohlcv_candles.set_index(['timestamp'], inplace=True)

        macd, signal, hist = talib.MACD(ohlcv_candles.close.values,
                                        fastperiod=8, slowperiod=28, signalperiod=9)
        
        # sell
        if hist[-2] > 0 and hist[-1] < 0:
            return -1 
        # buy
        elif hist[-2] < 0 and hist[-1] > 0:
            return 1
        # do nothing
        else:
            return 0
