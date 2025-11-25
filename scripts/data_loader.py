# scripts/data_loader.py
import pandas as pd
import yfinance as yf

def load_news_csv(path: str, date_col: str = "date") -> pd.DataFrame:
    """Load news CSV, parse date column."""
    df = pd.read_csv(path)
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    return df

def download_price(ticker: str, start: str = None, end: str = None) -> pd.DataFrame:
    """Download daily prices using yfinance and return DataFrame with Date and OHLCV."""
    df = yf.download(ticker, start=start, end=end, progress=False)
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    # keep consistent column names
    df = df.rename(columns=lambda s: s.capitalize())
    return df[["Date", "Open", "High", "Low", "Close", "Volume"]]
