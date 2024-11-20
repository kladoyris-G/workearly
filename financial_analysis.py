
import streamlit as st
from openai import OpenAI
import yfinance as yf
import datetime
from plotly import graph_objs as go

client = OpenAI(api_key="")

st.title('Interactive Financial Stock Market Comparative Analysis Tool')

# Function to fetch stock data and financial metrics
def get_stock_data(ticker, start_date='2024-01-01', end_date='2024-02-01'):
    data = yf.download(ticker, start=start_date, end=end_date)
    stock_info = yf.Ticker(ticker).info
    financials = {
        'Market Cap': stock_info.get('marketCap'),
        'P/E Ratio': stock_info.get('trailingPE'),
        'Dividend Yield': stock_info.get('dividendYield'),
        'Beta': stock_info.get('beta'),
    }
    return data, financials

# Sidebar for user inputs
st.sidebar.header('User Input Options')
selected_stock = st.sidebar.text_input('Enter Stock Ticker 1', 'AAPL').upper()
selected_stock2 = st.sidebar.text_input('Enter Stock Ticker 2', 'GOOGL').upper()

# Date range selection
start_date = st.sidebar.date_input('Start Date', datetime.date(2024, 1, 1))
end_date = st.sidebar.date_input('End Date', datetime.date(2024, 2, 1))

# Fetch stock data
stock_data, stock_financials = get_stock_data(selected_stock, start_date, end_date)
stock_data2, stock_financials2 = get_stock_data(selected_stock2, start_date, end_date)

col1, col2 = st.columns(2)

# Display stock data and financial metrics
with col1:
    st.subheader(f"Displaying data for: {selected_stock}")
    st.write("### Stock Data")
    st.write(stock_data)
    st.write("### Financial Metrics")
    st.write(stock_financials)
    
    chart_type = st.sidebar.selectbox(f'Select Chart Type for {selected_stock}', ['Line', 'Bar', 'Candlestick'])
    if chart_type == 'Line':
        st.line_chart(stock_data['Close'])
    elif chart_type == 'Bar':
        st.bar_chart(stock_data['Close'])
    elif chart_type == 'Candlestick':
        fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             open=stock_data['Open'],
                                             high=stock_data['High'],
                                             low=stock_data['Low'],
                                             close=stock_data['Close'])])
        st.plotly_chart(fig)

with col2:
    st.subheader(f"Displaying data for: {selected_stock2}")
    st.write("### Stock Data")
    st.write(stock_data2)
    st.write("### Financial Metrics")
    st.write(stock_financials2)
    
    chart_type2 = st.sidebar.selectbox(f'Select Chart Type for {selected_stock2}', ['Line', 'Bar', 'Candlestick'])
    if chart_type2 == 'Line':
        st.line_chart(stock_data2['Close'])
    elif chart_type2 == 'Bar':
        st.bar_chart(stock_data2['Close'])
    elif chart_type2 == 'Candlestick':
        fig2 = go.Figure(data=[go.Candlestick(x=stock_data2.index,
                                              open=stock_data2['Open'],
                                              high=stock_data2['High'],
                                              low=stock_data2['Low'],
                                              close=stock_data2['Close'])])
        st.plotly_chart(fig2)

if st.button('Comparative Performance'):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a financial assistant that will retrieve two tables of financial market data and will summarize the comparative performance in text, in full detail with highlights for each stock and also a conclusion with a markdown output. BE VERY STRICT ON YOUR OUTPUT"},
                {"role": "user", "content": f"This is the {selected_stock} stock data: {stock_data}, this is {selected_stock2} stock data: {stock_data2}"}
              ]
        )
    st.markdown(response.choices[0].message.content)

