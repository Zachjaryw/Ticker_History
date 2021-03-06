import pandas as pd
import datetime as dt
import yfinance
from pandas_datareader import data as pdr
import streamlit as st

end = dt.date.today().strftime('%Y-%m-%d') #Set end date for collection

st.title("Tickers Historical Data")
start = st.text_input("Input start date here: (Format YYYY-MM-DD)", '2021-01-01') #Allow user to chose own start date

st.write('For list of possible tickers, visit: https://tinyurl.com/NYSETickers')
tickers = st.text_input("Input tickers here: (Use comma to seperate tickers)",'AAPL') #Allow user to chose ticker symbol

breakdown = st.selectbox('Breakdown Historical data by:',['Day','Week','Month'])

#Collect Data
yfinance.pdr_override()
data = pd.DataFrame()
data = pdr.get_data_yahoo(tickers, start=start, end=end)['Adj Close']

if breakdown == 'Day':
  pass
elif breakdown == 'Week':
  data = data.iloc[::5]
elif breakdown == 'Month':
  data = data.iloc[::22]
data = data.iloc[::-1]

#Display Data
st.header(f'Adjusted Closing Values per {breakdown}')
data = data.reset_index()
if data.shape[1] == 2:
  data = data.set_index('Date')
  st.write(data)
  st.line_chart(data)
if data.shape[1] > 2:
  data = data.set_index('Date')
  seperate1 = st.checkbox('Seperate Graphs? (Adj Close)')
  st.write(data)
  if seperate1 == True:
    for i in range(data.shape[1]):
      st.line_chart(data.iloc[:,i])
  elif seperate1 == False:
    st.line_chart(data)

change = pd.DataFrame({'Date':data.index})
data = data.reset_index()
if data.shape[1] == 2:
  ct = False
  list1 = data['Adj Close'].tolist()
  list2 = data['Adj Close'].tolist()
  list2.remove(list2[0]);list2.append(list2[-1])
  difference = []
  zip_object = zip(list1, list2)
  for list1_i, list2_i in zip_object:
      difference.append((list1_i-list2_i)/list1_i*100)
  dif = pd.DataFrame({'Adj Close':difference})
  change = pd.concat([change,dif],axis = 1)
  change = change.set_index('Date')
    
elif data.shape[1] > 2:
  ct = True
  data = data.set_index('Date')
  cols = data.columns
  for col in cols:
      list1 = data[col].tolist()
      list2 = data[col].tolist()
      list2.remove(list2[0]);list2.append(list2[-1])
      difference = []
      zip_object = zip(list1, list2)
      for list1_i, list2_i in zip_object:
          difference.append((list1_i-list2_i)/list1_i*100)
      dif = pd.DataFrame({'Difference':difference})
      change = pd.concat([change,dif],axis = 1)
  
#Display Accelaration Graph
st.header(f'Acceleration Graph of Closing Values per {breakdown}')
if ct == True:
  seperate = st.checkbox('Seperate Graphs? (Difference)')
  change = change.set_index('Date')
  change.columns = data.columns
  st.write(change)
  if seperate == True:
    for i in range(change.shape[1]):
      st.line_chart(change.iloc[:,i])
  elif seperate == False:
    st.line_chart(change)
elif ct == False:
  st.write(change)
  st.line_chart(change)
