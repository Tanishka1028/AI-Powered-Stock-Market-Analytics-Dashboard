import streamlit as st
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.indicators import (
    add_moving_averages,
    add_rsi,
    add_macd
)
from utils.prediction import predict_prices

st.set_page_config(
    page_title="AI Stock Dashboard",
    layout="wide"
)

st.title("📈 AI-Powered Stock Dashboard")

# Sidebar
st.sidebar.header("Settings")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

# Load data
with st.spinner("Loading stock data..."):

    df = load_data(ticker)

    df = add_moving_averages(df)

    df = add_rsi(df)

    df = add_macd(df)


# Candlestick Chart


st.subheader(f"{ticker} Candlestick Chart")

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlestick"
        )
    ]
)

# Add Moving Averages

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA50"],
        line=dict(width=2),
        name="50 MA"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA200"],
        line=dict(width=2),
        name="200 MA"
    )
)

fig.update_layout(
    height=700,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)


# Key Metrics


latest_close = df["Close"].iloc[-1]
latest_ma50 = df["MA50"].iloc[-1]
latest_ma200 = df["MA200"].iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Price",
    f"${latest_close:.2f}"
)

col2.metric(
    "50-Day MA",
    f"${latest_ma50:.2f}"
)

col3.metric(
    "200-Day MA",
    f"${latest_ma200:.2f}"
)


# Trend Analysis


st.subheader("Trend Analysis")

if latest_ma50 > latest_ma200:
    st.success("📈 Bullish Trend Detected")

else:
    st.error("📉 Bearish Trend Detected")


# RSI Chart


st.subheader("RSI Indicator")

rsi_fig = go.Figure()

rsi_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["RSI"],
        name="RSI"
    )
)

rsi_fig.add_hline(y=70)

rsi_fig.add_hline(y=30)

st.plotly_chart(rsi_fig, use_container_width=True)

latest_rsi = df["RSI"].iloc[-1]

if latest_rsi > 70:
    st.warning("⚠️ Stock is Overbought")

elif latest_rsi < 30:
    st.success("✅ Stock is Oversold")


# MACD Chart


st.subheader("MACD Indicator")

macd_fig = go.Figure()

macd_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MACD"],
        name="MACD"
    )
)

macd_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MACD_SIGNAL"],
        name="Signal"
    )
)

st.plotly_chart(macd_fig, use_container_width=True)


# AI Prediction


st.subheader("AI Price Prediction")

prediction = predict_prices(df)

st.metric(
    "Predicted Next Closing Price",
    f"${prediction:.2f}"
)