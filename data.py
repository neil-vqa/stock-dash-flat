import pandas as pd
import numpy as np
from iexfinance.stocks import get_market_most_active
from iexfinance.stocks import get_market_gainers
from iexfinance.stocks import get_market_losers
import yfinance as yf

iex_key = 'pk_e682e00599c744d9bb4d6686d4ee7549'

def data_parse():
	data = get_market_gainers(token=iex_key)
	datax = get_market_losers(token=iex_key)
	datay = get_market_most_active(token=iex_key)

	symbol = [data[0]['symbol'],data[1]['symbol'],data[2]['symbol']]
	df = yf.download(symbol,period='6mo',interval='1d',group_by='ticker',auto_adjust=True)

	data1 = df[symbol[0]]
	data2 = df[symbol[1]]
	data3 = df[symbol[2]]

	return data,datax,datay,data1,data2,data3,symbol

