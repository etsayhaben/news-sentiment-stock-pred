import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.stats import pearsonr
from typing import Tuple

analyzer = SentimentIntensityAnalyzer()

def add_vader_scores(df: pd.DataFrame, text_col: str = "headline") -> pd.DataFrame:
    """Add VADER compound score column 'sentiment' to news dataframe."""
    df = df.copy()
    df[text_col] = df[text_col].astype(str)
    df["sentiment"] = df[text_col].apply(lambda t: analyzer.polarity_scores(t)["compound"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

def aggregate_daily_sentiment(df_news: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment by stock and calendar date."""
    df = df_news.copy()
    df["day"] = df["date"].dt.date
    agg = df.groupby(["stock", "day"], as_index=False)["sentiment"].mean().rename(columns={"sentiment":"daily_sentiment"})
    agg["day"] = pd.to_datetime(agg["day"])
    return agg

def compute_daily_returns(df_prices: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns from price DataFrame with columns Date and Close."""
    df = df_prices.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["daily_return"] = df["Close"].pct_change()
    return df

def merge_sentiment_prices(df_sent: pd.DataFrame, df_price: pd.DataFrame, stock: str) -> pd.DataFrame:
    """Merge aggregated sentiment and price returns for a single stock."""
    df_s = df_sent[df_sent["stock"] == stock].copy()
    df_p = df_price.copy()
    df_p["day"] = df_p["Date"].dt.normalize()
    df_s["day"] = pd.to_datetime(df_s["day"]).dt.normalize()
    merged = pd.merge(df_p, df_s, on="day", how="left")
    merged = merged.sort_values("Date")
    return merged

def correlation_sentiment_returns(merged_df: pd.DataFrame) -> Tuple[float, float]:
    """Compute Pearson correlation between daily_sentiment and daily_return (drops NaNs). Returns r and p-value."""
    df = merged_df.dropna(subset=["daily_sentiment", "daily_return"])
    if len(df) < 3:
        return float("nan"), float("nan")
    r, p = pearsonr(df["daily_sentiment"], df["daily_return"])
    return float(r), float(p)