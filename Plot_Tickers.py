import pandas as pd
import datetime as dt
import yfinance
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import streamlit as st

today = dt.date.today().strftime('%Y-%m-%d')
end = today

st.title("Tickers Historical Data")
start = st.text_input("Input start date here:", '2020-01-01')
tickers = st.text_input("Input tickers here:",'AAPL')

yfinance.pdr_override()
data = pd.DataFrame()

data = pdr.get_data_yahoo(tickers, start=start, end=end)['Adj Close']

data = data.iloc[::-1]
st.header('Adjusted Closing Values per Day')
st.write(data)
st.line_chart(data)
