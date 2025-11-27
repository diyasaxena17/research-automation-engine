import sys
from data_ingest import load_data
from signals import compute_all_signals
from report import normalize_dict, summarize_signals, format_table
import yfinance as yf
from report import sparkline
import pandas as pd



def main():
    if len(sys.argv) < 2:
        print("Usage: python research.py <TICKER>")
        sys.exit(1)

    ticker = sys.argv[1].upper()

    print(f"\nFetching data for {ticker}...")
    df = load_data(ticker)

    print("Fetching benchmark (SPY)...")
    spy = yf.download("SPY", period="1y", progress=False)

    print("\nComputing signals...")
    raw = compute_all_signals(df, spy)
    norm = normalize_dict(raw)

    print("\n=== SIGNAL TABLE ===\n")
    print(format_table(raw, norm))

   # 1-year price sparkline
    # 1-year price sparkline
    # Ensure price is always a Series, even if yfinance returns multi-index columns
    price_series = df["Close"]

    # If it's a DataFrame (multi-column), squeeze it into a Series
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.squeeze("columns")

    prices = price_series.tail(60).tolist()

    trend = sparkline(prices)


    print("\n=== TREND ===\n")
    print(f"Price Trend (Last 60 Days):\n{trend}\n")

    print("\n=== SUMMARY ===\n")
    print(summarize_signals(ticker, raw, norm))



if __name__ == "__main__":
    main()
