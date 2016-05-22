class Company:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

class Symbol:
    #handling change data for MAs
    PCTChange200Day = 0
    Change200Day = 0
    PCTChangeYear = 0
    PCTChange50Day = 0
    Change50Day = 0
    
    #moving average data
    MA200Day = 0
    MA50Day = 0
    
    #EPS Estimates
    
    
    def __init__(self, symbol, ask, bid, open):
        self.symbol = symbol
        self.ask = ask
        self.bid = bid
        self.open = open
        
        
        