from QuantLib import *
import csv
import json
from optionchain import OptionChain
from googlefinance import *
import numpy as np
import pyflux as pf
import pandas as pd
from pandas.io.data import DataReader
from datetime import datetime
import matplotlib.pyplot as plt

#This file has been adapted from a quantlib example in python.



#where each is the following:
#Today's date, date of option purchase
#Expiry date, date of option expiry
#vol is calclulated volatility value
#opttype is either a put or call option
#underlying price is current price of the equity
#strike price is price of option to be sold
def EstimateOption(todaysDate, expiryDate, vol, opttype, underlying, strike):
    # global data
    Settings.instance().evaluationDate = todaysDate
    settlementDate = todaysDate
    riskFreeRate = FlatForward(settlementDate, 0.06, Actual365Fixed())

    # option parameters
    exercise = AmericanExercise(settlementDate, expiryDate)
    payoff = PlainVanillaPayoff(opttype, strike)

    # market data
    underlying = SimpleQuote(underlying)
    volatility = BlackConstantVol(todaysDate, UnitedStates(), vol, Actual365Fixed())
    dividendYield = FlatForward(settlementDate, 0.00, Actual365Fixed())


    # good to go

    process = BlackScholesMertonProcess(QuoteHandle(underlying),
                                        YieldTermStructureHandle(dividendYield),
                                        YieldTermStructureHandle(riskFreeRate),
                                        BlackVolTermStructureHandle(volatility))
    
    results = []
    option = VanillaOption(payoff, exercise)
    option.setPricingEngine(BaroneAdesiWhaleyEngine(process))
    results.append(round(option.NPV(),3))
    option.setPricingEngine(BjerksundStenslandEngine(process))
    results.append(round(option.NPV(),3))
    
    timeSteps = 801
    gridPoints = 800
    option.setPricingEngine(FDAmericanEngine(process,timeSteps,gridPoints))
    results.append(round(option.NPV(),3))
    
    timeSteps = 801
    option.setPricingEngine(BinomialVanillaEngine(process,'jr',timeSteps))
    results.append(round(option.NPV(),3))
    option.setPricingEngine(BinomialVanillaEngine(process,'crr',timeSteps))
    results.append(round(option.NPV(),3))
    option.setPricingEngine(BinomialVanillaEngine(process,'eqp',timeSteps))
    results.append(round(option.NPV(),3))
    option.setPricingEngine(BinomialVanillaEngine(process,'trigeorgis',timeSteps))
    results.append(round(option.NPV(),3))
    option.setPricingEngine(BinomialVanillaEngine(process,'tian',timeSteps))
    results.append(round(option.NPV(),3))
    option.setPricingEngine(BinomialVanillaEngine(process,'lr',timeSteps))
    results.append(round(option.NPV(),3))
    
    return results

def main():
    symbols = import_from_csv()
    print symbols
    with open('simputs.csv', 'wb',) as currdata:
        writer = csv.writer(currdata, delimiter=',')
        for i in symbols:
            oc = OptionChain('NASDAQ:' + i)
            underlying = float(getQuotes(i)[0]['LastTradeWithCurrency'])
            stock = DataReader(i, 'yahoo', datetime(2014,1,1), datetime(2016,6,1))
            returns = pd.DataFrame(np.diff(np.log(stock['Adj Close'].values)))
            model = pf.GARCH(abs(returns), p=1, q=1)
            x = model.fit()
            vol = float(model.predict(h=7)['0'].values.tolist()[-1]) * float(100)
            for j in oc.puts:
                strike = float(j['strike'])
                if (str(j['p']) != '-'):
                    opttype = Option.Put
                    todaysDate = Date(4,June,2016)
                    expiryDate = Date(10,June,2016)
                    print('-'*32)
                    print(i)
                    print(j['s'])
                    print(str(j['strike']))
                    print(str(j['p']))
                    results = EstimateOption(todaysDate, expiryDate, vol, opttype, underlying,strike)
                    writer.writerow([str(i), str(j['s']), str(j['strike']), str(j['p'])] + results)

#imports all relevant stock symbols from CSV
def import_from_csv():
    symbols = []
    with open('symbols.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            symbols.append(row[0])
    return symbols
            
if __name__ == '__main__':
    main()
