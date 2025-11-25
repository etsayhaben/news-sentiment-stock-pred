# Project: Predicting Price Moves with News Sentiment

Contents:
- notebooks/sentiment.py : sentiment aggregation & correlation utilities
- notebooks/indicators.py : technical indicator utilities
- scripts/data_loader.py : loaders for news CSV and yfinance prices
- tests/ : unit tests

Quick usage (Windows PowerShell):
1. python -m pip install -r requirements.txt
2. pytest -q

Notes:
- Place your news CSV under c:\Users\haben\Downloads\Compressed\data\ and update paths in notebooks or scripts as needed.