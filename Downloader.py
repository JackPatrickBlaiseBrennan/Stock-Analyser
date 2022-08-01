from datetime import date, timedelta
from yahoo_fin.stock_info import get_data, tickers_nasdaq
import warnings
import time
from os.path import exists as file_exists

class Downloader:
    __STOCK_FOLDER = "Stocks/"
    
    def __init__(self):
        self.__getDates()
        self.__get_nasdaq_tickers()
        print("Amount of Tickers: ", len(self.__tickers))
        self.__download_all_ticker_data()
        
        
    def __getDates(self):
        today = date.today()
        yearAgo = today - timedelta(days=365)
        self.__today = today.strftime("%d/%m/%Y")
        self.__yearAgo = yearAgo.strftime("%d/%m/%Y")
        warnings.simplefilter(action='ignore', category=UserWarning)

    def __get_nasdaq_tickers(self):
        self.__tickers = tickers_nasdaq()
    
    def __download_single_ticker_data(self, ticker):
        try:
            print("Getting Data For: ", ticker)
            dataFrame = get_data(ticker, start_date=self.__yearAgo, end_date=self.__today, index_as_date=True, interval="1d")
            time.sleep(2)
            finalFile = self.__STOCK_FOLDER + ticker.replace(".", "_") + ".csv"
            dataFrame.to_csv(finalFile)
            print(finalFile, " Saved")
        except Exception as ex:
            print("Unable to get data for:", ticker)
    
    def __download_all_ticker_data(self):
        for ticker in self.__tickers:
            if not (file_exists(self.__STOCK_FOLDER + ticker + ".csv")):
                self.__download_single_ticker_data(ticker)
                print("Done")

    def getTickers(self):
        return self.__tickers
    
if __name__ == "__main__":
    d = Downloader()
    
        