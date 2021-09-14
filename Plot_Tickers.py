import pandas as pd
import datetime as dt
import yfinance
from pandas_datareader import data as pdr
import streamlit as st

end = dt.date.today().strftime('%Y-%m-%d') #Set end date for collection

st.title("Tickers Historical Data")
start = st.text_input("Input start date here:", '2021-01-01') #Allow user to chose own start date
#start = DateTime.ParseExact(start, '%Y-%m-%d')
st.write('For list of possible tickers, visit: https://tinyurl.com/NYSETickers')
tickers = st.text_input("Input tickers here:",'AAPL') #Allow user to chose ticker symbol

#Collect Data
yfinance.pdr_override()
data = pd.DataFrame()
data = pdr.get_data_yahoo(tickers, start=start, end=end)['Adj Close']
data = data.iloc[::-1]

#Display Data
st.header('Adjusted Closing Values per Day')
st.write(data)
st.line_chart(data)
