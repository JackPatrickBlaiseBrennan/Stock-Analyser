import pandas as maniplation

class StockAnalyser:
    __STOCK_FOLDER = "Stocks/"
    
    def __init__(self, tickers):
        self.__tickers = tickers
        self.add_analytics_to_all_tickers()
        
    def get_dataframe_from_csv(self, ticker):
        try:
            dataFrame = maniplation.read_csv(self.__STOCK_FOLDER + ticker + ".csv", index_col=0)
        except FileNotFoundError:
            print("File Not Found")
        else:
            return dataFrame
    
    def add_daily_returns(self, dataframe):
        dataframe['daily_return'] = (dataframe['close'] / dataframe['close'].shift(1)) - 1
        return dataframe

    def add_cumulative_returns(self, dataframe):
        dataframe['cumulative_return'] = (1 + dataframe['daily_return']).cumprod()
        return dataframe
    
    def add_bollinger_bands(self, dataframe):
        dataframe['middle_band'] = dataframe['close'].rolling(window=20).mean()
        dataframe['upper_band'] = dataframe['middle_band'] + 1.96 * dataframe['close'].rolling(window=20).std()
        dataframe['lower_band'] = dataframe['middle_band'] - 1.96 * dataframe['close'].rolling(window=20).std()
        return dataframe
    
    def add_ichimoku(self, dataframe):
        high9 = dataframe['high'].rolling(window=9).max()
        low9 = dataframe['low'].rolling(window=9).min()
        dataframe['Conversion'] =  (high9 + low9) / 2
        
        high26 = dataframe['high'].rolling(window=26).max()
        low26 = dataframe['low'].rolling(window=26).min()
        dataframe['Baseline'] =  (high26 + low26) / 2
        dataframe['SpanA'] = (dataframe['Conversion'] + dataframe['Baseline']) / 2
        
        high52 = dataframe['high'].rolling(window=52).max()
        low52 = dataframe['low'].rolling(window=52).min()
        dataframe['SpanB'] = ((high52 + low52) / 2).shift(26)
        
        dataframe['Lagging'] = dataframe['close'].shift(-26)
        return dataframe
    
    def add_analytics_to_single_ticker(self, ticker):
        print("Adding Analytics to :", ticker)
        dataframe = self.get_dataframe_from_csv(ticker)
        if (dataframe is not None):
            dataframe = self.add_daily_returns(dataframe)
            dataframe = self.add_cumulative_returns(dataframe)
            dataframe = self.add_bollinger_bands(dataframe)
            dataframe = self.add_ichimoku(dataframe)
            dataframe.to_csv(self.__STOCK_FOLDER + ticker + ".csv")
        
    def add_analytics_to_all_tickers(self):
        for ticker in self.__tickers:
            self.add_analytics_to_single_ticker(ticker)