### functions for visualization and analysis
### in the a python notebook

import numpy as np

## parses the simcalls.csv file
## returns a dictionary with key = (symbol, tag)
## and value = (Strike,Real,Barone-Adesi Whaley,Bjerksund-Stensland,FDAmerican,Cox-Ross-Rubenstein,Jarrow-Rudd,Equal Probabilities,Trigeorgis,Tian,Leisen-Reimer)
def parseSimCalls(filename):
    resultsDict = {}
    f = open(filename, 'r')
    raw = f.read()
    rawLines = raw.split('\n')
    for i in range(1,len(rawLines)):
        data = rawLines[i].strip().split(',')
        resultsDict[(data[0],data[1])] = (float(data[2]),float(data[3]),float(data[4]),float(data[5]),
                                          float(data[6]),float(data[7]),float(data[8]),float(data[9]),
                                          float(data[10]),float(data[11]),float(data[12]))
    return resultsDict
        
## parses the simputs.csv file
## returns a dictionary with key = (symbol, tag)
## and value = (Strike,Real,Barone-Adesi Whaley,Bjerksund-Stensland,FDAmerican,Cox-Ross-Rubenstein,Jarrow-Rudd,Equal Probabilities,Trigeorgis,Tian,Leisen-Reimer)
def parseSimPuts(filename):
    resultsDict = {}
    f = open(filename, 'r')
    raw = f.read()
    rawLines = raw.split('\n')
    for i in range(1,len(rawLines)):
        data = rawLines[i].strip().split(',')
        if data[5] == 'nan':
            resultsDict[(data[0],data[1])] = (float(data[2]),float(data[3]),float(data[4]),float('0'),
                                              float(data[6]),float(data[7]),float(data[8]),float(data[9]),
                                              float(data[10]),float(data[11]),float(data[12]))
        else:
            resultsDict[(data[0],data[1])] = (float(data[2]),float(data[3]),float(data[4]),float(data[5]),
                                              float(data[6]),float(data[7]),float(data[8]),float(data[9]),
                                              float(data[10]),float(data[11]),float(data[12]))
    return resultsDict    
 

## takes in a dictionary and index of estimate/class from tuple in dictionaries
## returns numpy array of real prices and estimates
def getRealEstimates(dataDict, col):
    real = []
    estimates = []
    for k in dataDict.keys():
        real.append(dataDict[k][1])
        estimates.append(dataDict[k][col])
    real = np.array(real)
    estimates = np.array(estimates)
    return real, estimates
    
# takes in np arrays of predictions and groundtruth
# returns the sum squared error
def sse(predicted, groundtruth):
    errors = predicted - groundtruth
    errors = errors**2
    
    return np.sum(errors)


# takes in np arrays of predictions and groundtruth
# returns the average sum squared error
def avgSSE(predicted, groundtruth):
    s = sse(predicted, groundtruth)
    return s/predicted.shape[0]


# takes in np arrays of predictions, groundtruth, and a threshold for range of error
# returns precentage of predictions with errors below that threshold
def thresholdAcc(predicted, groundtruth, e):
    errors = predicted - groundtruth
    total = predicted.shape[0]
    count = 0

    for i in range(len(errors)):
        if abs(errors[i]) <= e:
            count += 1
    return (count/total) * 100


# takes in np arrays of predictions and groundtruth
# returns precentage of predictions with the right sentiment
def sentimentAcc(predicted, groundtruth):
    predSign = np.sign(predicted)
    truthSign = np.sign(groundtruth)
    total = predicted.shape[0]
    count = 0
    for p, t in zip(predSign, truthSign):
        if p == t:
            count += 1
    return (count/total) * 100
