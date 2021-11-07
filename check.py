import sys
import json
import pytz
import numpy as np
import pandas as pd
from pandas import merge_ordered
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import talib
import time
from mychart import myLineChart
from tabulate import tabulate
import glob

if(len(sys.argv)>2):
    granularity = sys.argv[1]
    symbols = sys.argv[2:]
else:    
	list_of_files = glob.glob('./coinbase/*-3600.json')
	symbols = []
	for f in list_of_files:
		granularity = '3600'
		s_name = f.replace('-3600.json','').replace('./coinbase/','')
		symbols.append(s_name)

    
def getPrices(symbol):
    with open('coinbase/'+symbol+'-'+granularity+'.json', 'r', encoding='utf-8') as f:
        df = (pd.read_json(f))
    df['date'] = df['time']
    df.set_index('date')
    df.sort_values(by='date', inplace=True, ascending=True)    
    return df

def addPeaksandDips(prices):
	y = np.array(prices['close'])
	peaks = np.where((y[1:-1] > y[0:-2]) * (y[1:-1] > y[2:]))[0] + 1
	dips = np.where((y[1:-1] < y[0:-2]) * (y[1:-1] < y[2:]))[0] + 1
	myPeaks = []
	myDips=[]

	for idx in range(len(prices['close'])):
		if idx in peaks:
			myPeaks.append(1)
		else:
			myPeaks.append(0)
		if idx in dips:
			myDips.append(1)
		else:
			myDips.append(0)

	prices['peaks'] = myPeaks
	prices['dips'] = myDips
	prices['rsi'] = talib.RSI(prices['close'],timeperiod=13)

	return prices

def checkDivergences(df):
	cLen = len(df)
	divergencesDf = pd.DataFrame(columns=['date','rsi_divergence'])
	for idx in range(cLen-2):
		cPrev = df.iloc[-1-idx]
		cPrevPrev = df.iloc[-2-idx]
		if((cPrevPrev['close'] > cPrev['close']) and (cPrevPrev['rsi'] < cPrev['rsi'])):
			divergencesDf=divergencesDf.append({'date':cPrevPrev['date'],'rsi_divergence':1}, ignore_index=True)

		if((cPrevPrev['close'] < cPrev['close']) and (cPrevPrev['rsi'] > cPrev['rsi'])):
			divergencesDf = divergencesDf.append({'date':cPrevPrev['date'],'rsi_divergence':-1}, ignore_index=True)


	return divergencesDf

def checkW(df):
	peaks_df = df[df.peaks.eq(1)]
	last = df.iloc[-1]
	lpeak = peaks_df.iloc[-1]
	llpeak = peaks_df.iloc[-2]
	#go over 2 peaks
	cond1 = last['close'] > lpeak['close']
	cond2 = last['close'] > llpeak['close']

	dips_df = df[df.dips.eq(1)]
	ldip = dips_df.iloc[-1]
	lldip = dips_df.iloc[-2]
	cond3 = ldip['close'] >= lldip['close']

	if(cond1 and cond2 and cond3):
		return 1
	if((lpeak['close'] > llpeak['close']) and (ldip['close'] >= lldip['close']) and last['close']>llpeak['close']):
		return 2


def checkPriceValue(df):
	df=df.tail(90)#can check for 180 alt
	maxPrice = df['close'].max()
	minPrice = df['close'].min()
	last = df.iloc[-1]
	diffPrice = last['close'] - minPrice
	diffMax = maxPrice - minPrice
	percent = (diffPrice*100)/diffMax

	return percent

def get50percent(df):
    df=df.tail(90)
    maxPrice = df['close'].max()
    minPrice = df['close'].min()
    diff = (maxPrice-minPrice)
    return [minPrice+diff*0.5,minPrice+diff*0.618]

header = ["symbol","w","price location","[0.50]", "[0.618]"]
rowswithData = []

for symbol in symbols:
	pSorted = getPrices(symbol)
	if(len(pSorted)<1):
		continue

	sigChart = addPeaksandDips(pSorted)

	peaks_df = sigChart[sigChart.peaks.eq(1)]
	d1 = checkDivergences(peaks_df)

	dips_df = sigChart[sigChart.dips.eq(1)]
	d2 = checkDivergences(dips_df)

	divs = pd.concat([d1,d2])
	sigChart = (merge_ordered(sigChart, divs, left_by='date', fill_method="ffill"))
	xW = checkW(sigChart)
	valS = checkPriceValue(sigChart)
	levels = get50percent(sigChart)
	rowData = [symbol,xW,valS,levels[0],levels[1]]
	rowswithData.append(rowData)
	if(xW==1 and valS < 70):
		myLineChart(sigChart,symbol)

print(tabulate(rowswithData, headers=header, tablefmt='orgtbl'))
