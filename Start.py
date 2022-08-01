from Downloader import Downloader


from Downloader import *
from StockAnalyser import *

def start():
    downloader = Downloader()
    StockAnalyser(downloader.getTickers())

if __name__ == "__main__":
    start()