import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import requests

api_key = ""

def get_closing_price(ticker_symbol):
    
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        # outputsize compact returns last 100. full returns full timeseries
        data, meta_data = ts.get_intraday(symbol=ticker_symbol, interval="1min", outputsize = 'compact') 
        return data['4. close'].iloc[0]
    except ValueError:
        return "API Error"

def get_company_name(ticker_symbol):
    
    API_URL = "https://www.alphavantage.co/query" 

    data = { 
        "function": "OVERVIEW", 
        "symbol": ticker_symbol,
        "outputsize" : "compact",
        "datatype": "json", 
        "apikey": api_key
        } 

    try:
        response = requests.get(API_URL, data) 
        response_json = response.json()
        return (response_json['Name'])
    except KeyError:
        return "API Error"