import pandas as pd
import numpy as np

def sma(df: pd.DataFrame, window: int, price_col: str = "Close") -> pd.Series:
    return df[price_col].rolling(window).mean()

def ema(df: pd.DataFrame, span: int, price_col: str = "Close") -> pd.Series:
    return df[price_col].ewm(span=span, adjust=False).mean()

def rsi(df: pd.DataFrame, period: int = 14, price_col: str = "Close") -> pd.Series:
    delta = df[price_col].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, price_col: str = "Close") -> pd.DataFrame:
    ema_fast = ema(df, fast, price_col)
    ema_slow = ema(df, slow, price_col)
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return pd.DataFrame({"macd": macd_line, "signal": signal_line, "hist": hist})

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sma_10"] = sma(df, 10)
    df["sma_50"] = sma(df, 50)
    df["rsi_14"] = rsi(df, 14)
    macd_df = macd(df)
    macd_df = macd_df.reset_index(drop=True)
    df = pd.concat([df.reset_index(drop=True), macd_df], axis=1)
    return df