import pandas as maniplation
import time
import requests
import yfinance as finaceapi
from tqdm import tqdm as loadingbar

class Downloader:
    __URL = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
    __STOCK_FOLDER = "Stocks/"
    __TICKER_FILE = __STOCK_FOLDER + "Nasdaq.csv"
    
    def __init__(self):
        self.__tickers = self.__scrap_csv("Symbol")
        print("Amount of Tickers: ", len(self.__tickers))
        self.__download_all_ticker_data()
        
    def __get_nasdaq_tickers(self):
        download = requests.get(self.__URL, stream =True)
        with open(self.__TICKER_FILE, "wb") as handle:
            for data in loadingbar(download.iter_content()):
                handle.write(data)
        
    def __scrap_csv(self, columnName):
        try:
            dataFrame = maniplation.read_csv(self.__TICKER_FILE)
        except FileNotFoundError:
            self.__get_nasdaq_tickers()
            return self.__scrap_csv(columnName)
        else:
            return dataFrame[columnName]
        
    def __download_single_ticker_data(self, ticker):
        stock = finaceapi.Ticker(ticker)
        
        try:
            print("Getting Data For: ", ticker)
            dataFrame = stock.history(peroid="max")
            time.sleep(2)
            
            finalFile = self.__STOCK_FOLDER + ticker.replace(".", "_") + ".csv"
            dataFrame.to_csv(finalFile)
            print(finalFile, " Saved")
        except Exception as ex:
            print("Unable to get data for:", ticker)
    
    def __download_all_ticker_data(self):
        for ticker in self.__tickers:
            self.__download_single_ticker_data(ticker)
            print("Done")

if __name__ == "__main__":
    d = Downloader()
    
        