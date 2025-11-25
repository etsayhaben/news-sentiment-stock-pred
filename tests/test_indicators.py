import pandas as pd
import numpy as np
from notebooks.indicators import add_indicators

def test_indicators_columns():
    prices = pd.DataFrame({
        "Date": pd.date_range("2021-01-01", periods=60),
        "Close": (100 + np.random.randn(60)).cumsum()
    })
    df = add_indicators(prices)
    assert "sma_10" in df.columns
    assert "rsi_14" in df.columns
    assert "macd" in df.columns