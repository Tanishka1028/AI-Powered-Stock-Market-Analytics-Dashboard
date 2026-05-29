import yfinance as yf
import streamlit as st

@st.cache_data

def load_data(ticker):
    stock = yf.Ticker(ticker)

    df = stock.history(period='2y')

    return df