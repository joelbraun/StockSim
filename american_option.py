from QuantLib import *
import csv
import json

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

    # report
    header = '%19s' % 'method' + ' |' + \
            ' |'.join(['%17s' % tag for tag in ['value',
                                                'estimated error',
                                                'actual error' ] ])
    print
    print header
    print '-'*len(header)

    refValue = None
    def report(method, x, dx = None):
        e = '%.4f' % abs(x-refValue)
        x = '%.5f' % x
        if dx:
            dx = '%.4f' % dx
        else:
            dx = 'n/a'
        print '%19s' % method + ' |' + \
            ' |'.join(['%17s' % y for y in [x, dx, e] ])

    # good to go

    process = BlackScholesMertonProcess(QuoteHandle(underlying),
                                        YieldTermStructureHandle(dividendYield),
                                        YieldTermStructureHandle(riskFreeRate),
                                        BlackVolTermStructureHandle(volatility))

    option = VanillaOption(payoff, exercise)

    refValue = 4.48667344
    report('reference value',refValue)

    # method: analytic

    option.setPricingEngine(BaroneAdesiWhaleyEngine(process))
    report('Barone-Adesi-Whaley',option.NPV())

    option.setPricingEngine(BjerksundStenslandEngine(process))
    report('Bjerksund-Stensland',option.NPV())

    # method: finite differences
    timeSteps = 801
    gridPoints = 800

    #option.setPricingEngine(FDAmericanEngine(process,timeSteps,gridPoints))
    report('finite differences',option.NPV())

    # method: binomial
    timeSteps = 801

    option.setPricingEngine(BinomialVanillaEngine(process,'jr',timeSteps))
    report('binomial (JR)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'crr',timeSteps))
    report('binomial (CRR)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'eqp',timeSteps))
    report('binomial (EQP)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'trigeorgis',timeSteps))
    report('bin. (Trigeorgis)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'tian',timeSteps))
    report('binomial (Tian)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'lr',timeSteps))
    report('binomial (LR)',option.NPV())

#def GenerateOptionData()


def main():
    symbols = import_from_csv()
    print symbols
    #for i in symbols:
    #    url = 'http://www.google.com/finance/option_chain?q=' + i + '&output=json&expy=2016&expm=' '&expd='
    #    response = urllib.request.urlopen()
    #for i in tocalculate:
    #or how it would be
    todaysDate = Date(27,May,2016)
    expiryDate = Date(3,June,2016)
    vol = .26
    underlying = 99.96
    opttype = Option.Call
    strike = 97.5
    
    EstimateOption(todaysDate, expiryDate, vol, opttype, underlying, strike)

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
