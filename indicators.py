from ta.momentum import RSIIndicator
from ta.trend import MACD


def add_moving_averages(df):

    df["MA50"] = df["Close"].rolling(window=50).mean()

    df["MA200"] = df["Close"].rolling(window=200).mean()

    return df

def add_rsi(df):

    rsi = RSIIndicator(close=df["Close"])

    df["RSI"] = rsi.rsi()

    return df

def add_macd(df):

    macd = MACD(close=df["Close"])

    df["MACD"] = macd.macd()

    df["MACD_SIGNAL"] = macd.macd_signal()

    return df