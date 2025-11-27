import streamlit as st
from data_ingest import load_data
from signals import compute_all_signals
from report import normalize_dict, summarize_signals, sparkline
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Research Automation Engine", layout="wide")

st.title("📈 Research Automation Engine (RAE)")
st.write("A simple quant research tool that computes signals and generates summaries.")

ticker = st.text_input("Enter Ticker Symbol", "AAPL").upper()

if st.button("Run Analysis"):

    with st.spinner("Fetching data..."):
        df = load_data(ticker)
        spy = yf.download("SPY", period="1y", progress=False)

    with st.spinner("Computing signals..."):
        raw = compute_all_signals(df, spy)
        norm = normalize_dict(raw)

    # Sparkline
    price_series = df["Close"]
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.squeeze("columns")
    prices = price_series.tail(60).tolist()

    st.subheader("📉 Price Trend (Last 60 Days)")
    st.code(sparkline(prices), language="text")

    # Table
    st.subheader("📊 Quant Signals")
    st.dataframe(pd.DataFrame({"Raw": raw, "Normalized": norm}))

    # Summary
    st.subheader("📝 Research Summary")
    st.write(summarize_signals(ticker, raw, norm))
