import sys
import json
import pytz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import talib
import time

if(len(sys.argv)>2):
    granularity = sys.argv[1]
    symbol = sys.argv[2:]    
else:
    print("symbol not passed")
    sys.exit(1)


def plotGraph(x,y):        
    plt.style.use('seaborn-whitegrid')
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = "10"
    plt.xticks(rotation=45)    
    for idx, el in enumerate(y):        
        plt.annotate('{0:.2f}'.format(el),(x[idx],y[idx]))
    
    peaks = np.where((y[1:-1] > y[0:-2]) * (y[1:-1] > y[2:]))[0] + 1
    peaksI = np.array(peaks)
    dips = np.where((y[1:-1] < y[0:-2]) * (y[1:-1] < y[2:]))[0] + 1
    dipsI = np.array(dips)
    
    
    

    plt.plot (x, y)
    plt.plot (x[peaksI], y[peaksI], 'o')
    plt.plot (x[dipsI], y[dipsI], 'o')

    plt.show()
    

def checkBullish(symbol):
    print(symbol)
    
    with open('coinbase/'+symbol+'-'+granularity+'.json', 'r', encoding='utf-8') as f:
        prices_panda = (pd.read_json(f))
    
    prices=[]
    prices_time = []
    for p in (prices_panda['close']):        
        prices.append(p)

    for p in (prices_panda['time']):        
        prices_time.append(p)
    
    prices = prices[:30]    
    prices_time = prices_time[:30]

    prices.reverse()
    prices_time.reverse()
    ta_serie = pd.DataFrame({'close':prices})

    
    
    draft_y = np.asarray(prices)
    y = draft_y.astype(float)    
    x = np.asarray(prices_time)
    x = np.array(x)
    
    
    #plotGraph(x,y)
    
    peaks = np.where((y[1:-1] > y[0:-2]) * (y[1:-1] > y[2:]))[0] + 1
    dips = np.where((y[1:-1] < y[0:-2]) * (y[1:-1] < y[2:]))[0] + 1
    
    lastDipIndex = len(dips)-1
    lastPeakIndex = len(peaks)-1

    pricePeakI1 = peaks[lastPeakIndex]
    pricePeakI2 = peaks[lastPeakIndex-1]

    priceDipI1 = dips[lastDipIndex]
    priceDipI2 = dips[lastDipIndex-1]

    if(
        prices[dips[lastDipIndex]] >= prices[dips[lastDipIndex-1]] and  
        prices[dips[lastDipIndex-1]] >= prices[dips[lastDipIndex-2]]
        ):
        print('3 H L ')

    #check a potential divergence
    rsis = talib.RSI(y,timeperiod=13)
    if(prices[pricePeakI1] > prices[pricePeakI2]):
        if(rsis[pricePeakI1] < rsis[pricePeakI2]):
            print("RSI down - Bear div "+str(rsis[pricePeakI1])+" / "+str(rsis[pricePeakI2]))        
    else:
        if(rsis[pricePeakI1] > rsis[pricePeakI2]):
            print("RSI UP - Bullish div "+str(rsis[pricePeakI1])+" / "+str(rsis[pricePeakI2]))

    #check for M
    low1 = prices[priceDipI1]
    low2 = prices[priceDipI2]
    lastClose = prices[len(prices)-1]
    if(lastClose<low1 and lastClose<low2):
        print("M")
    #check for w
    high1 = prices[pricePeakI1]
    high2 = prices[pricePeakI2]
    if(high1>=high2 and lastClose > high1):
        print("W")
list(map(lambda x:checkBullish(x),symbol))
