from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class SentinelTactical(IStrategy):
    INTERFACE_VERSION = 3
    minimal_roi = {"0": 0.01}
    stoploss = -0.05
    timeframe = '5m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['sma9'] = ta.SMA(dataframe, timeperiod=9)
        dataframe['sma21'] = ta.SMA(dataframe, timeperiod=21)
        dataframe['macd'] = ta.MACD(dataframe)['macd']
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['sma9'] > dataframe['sma21']) &
            (dataframe['macd'] > 0),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['sma9'] < dataframe['sma21']) &
            (dataframe['macd'] < 0),
            'exit_long'] = 1
        return dataframe