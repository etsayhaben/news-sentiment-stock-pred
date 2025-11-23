# scripts/data_loader.py
import pandas as pd
import yfinance as yf

def load_news(path="data/raw_analyst_ratings.csv"):
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.dropna(subset=["headline","stock"])
    return df

def download_stock(ticker, start, end):
    return yf.download(ticker, start=start, end=end)
