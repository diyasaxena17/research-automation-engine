import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def load_data(ticker: str) -> pd.DataFrame:
    """
    Downloads 1 year of daily OHLCV data for a given ticker.
    """
    end = datetime.today()
    start = end - timedelta(days=365)

    df = yf.download(ticker, start=start, end=end, progress=False)

    if df.empty:
        raise ValueError(f"Failed to download data for {ticker}")

    df = df.dropna()
    return df
