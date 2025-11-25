import pandas as pd
from notebooks.sentiment import add_vader_scores, aggregate_daily_sentiment, compute_daily_returns, merge_sentiment_prices, correlation_sentiment_returns

def test_sentiment_flow():
    news = pd.DataFrame({
        "headline": ["Good earnings beat", "Bad outlook", "Neutral comment"],
        "date": ["2021-01-04 09:00:00", "2021-01-05 10:00:00", "2021-01-05 13:00:00"],
        "stock": ["TST", "TST", "TST"]
    })
    news = add_vader_scores(news)
    daily = aggregate_daily_sentiment(news)
    prices = pd.DataFrame({
        "Date": pd.to_datetime(["2021-01-04", "2021-01-05"]),
        "Close": [100.0, 101.0]
    })
    prices = compute_daily_returns(prices)
    merged = merge_sentiment_prices(daily, prices, "TST")
    r, p = correlation_sentiment_returns(merged)
    assert isinstance(r, float)