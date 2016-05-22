#import numpy as np
from datamodel import *
import csv
from stockex import stockwrapper as sw
import concurrent.futures
import urllib.request
import time
NYSEsym = []
URLS = []

def getNYSESymbols():
    with open('companylist.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        NYSEsym.append(row[0])
        
def AssembleTrades(data):
    for i in data:
        if 

def main():
    data = sw.YahooData()
    getNYSESymbols()
    symData = loadSymbolDataRemote()
    AssembleTrades()
    
         

def load_ticker(symbol):
    time.sleep(0.25)
    tdata = data.get_current([symbol])
    s = Symbol(tdata['Symbol'], float(tdata['Ask']), float(tdata['Bid']), float(tdata['Open']))
    s.PCTChange200Day = float(tdata['PercentChangeFromTwoHundreddayMovingAverage'][:-1])
    s.Change200Day = float(tdata[ 'ChangeFromTwoHundreddayMovingAverage'])
    s.PCTChange50Day = float(tdata['PercentChangeFromFiftydayMovingAverage'][:-1])
    s.Change50Day = float(tdata['ChangeFromFiftydayMovingAverage'])
    
    #moving average data
    s.MA200Day = float(tdata['TwoHundreddayMovingAverage'])
    s.MA50Day = float(tdata['FiftydayMovingAverage'])
    return s
    
def loadSymbolDataRemote():
    tres = []  
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_ticker, sym): sym for sym in NYSEsym}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                res = future.result()
                tres.append(res)
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            
    with open('chartdata.csv', 'w', newline='') as currdata:
        writer = csv.writer(currdata, delimiter=',')
        for s in tres:
            writer.writerow([s.symbol, s.ask, s.bid, s.open,
            s.PCTChange200Day, s.Change200Day, s.PCTChange50Day, s.Change50Day,
            s.MA200Day, s.MA50Day])
    return tres

if __name__ == "__main__":
    main()