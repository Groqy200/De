import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import requests
import bs4
import numpy as np
import base64
import io

def get_financials(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/financials?p={symbol}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "W(100%)"})
    rows = []
    for tr in table.find_all("tr"):
        cols = tr.find_all("td")
        cols = [col.text.strip() for col in cols]
        if cols:
            rows.append(cols)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df

def get_sentiment(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/community?p={symbol}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "M(0) Whs(n) Bdcl(c)"})
    rows = []
    for tr in table.find_all("tr"):
        cols = tr.find_all("td")
        cols = [col.text.strip() for col in cols]
        if cols:
            rows.append(cols)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df

def bollinger_bands(data, window):
    std = data.rolling(window).std()
    upper_band = data.rolling(window).mean() + (std * 2)
    lower_band = data.rolling(window).mean() - (std * 2)
    return upper_band, lower_band

def rsi(data, window):
    delta = data.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def macd(data, short_window, long_window):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line, signal_line

st.set_page_config(page_title="Financial Analysis", page_icon=":chart_with_upwards_trend:", layout="wide")

st.title("Financial Analysis")
st.subheader("Enter a symbol to analyze (e.g., Bajaj, NSE:BAJAJFINSV, ^NSEI, BANKNIFTY, BANKNIFTY1!, NIFTYBANK!, NIFTY!):")

symbol = st.text_input("Symbol", "Bajaj")

if symbol:
    try:
        data = yf.download(symbol, start="2020-01-01", auto_adjust=True)

        st.subheader("Technical Analysis")
        st.write(data.describe())

        st.plotly_chart(go.Candlestick(x=data.index,
                                      open=data["Open"],
                                      high=data["High"],
                                      low=data["Low"],
                                      close=data["Close"]))

        st.subheader("Bollinger Bands")
        upper_band, lower_band = bollinger_bands(data["Close"], 20)
        st.plotly_chart(go.Scatter(x=data.index,
                                    y=upper_band,
                                    mode="lines",
                                    name="Upper Band",
                                    line=dict(color="green")))
        st.plotly_chart(go.Scatter(x=data.index,
                                    y=lower_band,
                                    mode="lines",
                                    name="Lower Band",
                                    line=dict(color="red")))

        st.subheader("RSI")
        rsi_data = rsi(data["Close"], 14)
        st.plotly_chart(go.Scatter(x=data.index,
                                    y=rsi_data,
                                    mode="lines",
                                    name="RSI",
                                    line=dict(color="blue")))

        st.subheader("MACD")
        macd_line, signal_line = macd(data["Close"], 12, 26)
        st.plotly_chart(go.Scatter(x=data.index,
                                    y=macd_line,
                                    mode="lines",
                                    name="MACD",
                                    line=dict(color="green")))
        st.plotly_chart(go.Scatter(x=data.index,
                                    y=signal_line,
                                    mode="lines",
                                    name="Signal Line",
                                    line=dict(color="red")))

        st.subheader("Fundamental Analysis")
        financials = get_financials(symbol)
        st.write(financials)

        st.subheader("Sentiment Analysis")
        sentiment = get_sentiment(symbol)
        st.write(sentiment)

    except Exception as e:
        st.error(f"Error: {e}")
