import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from data_ingest import load_data
from signals import compute_all_signals
from report import normalize_dict, summarize_signals, sparkline

# PAGE CONFIG + THEME
st.set_page_config(
    page_title="Research Engine",
    page_icon="📈",
    layout="wide"
)

# Global CSS styling
st.markdown("""
<style>
    body {
        background-color: #f7f9fc;
    }
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #f7f9fc;
    }
</style>
""", unsafe_allow_html=True)


# HERO HEADER
st.markdown("""
<div style="text-align:center; padding: 20px 0;">
    <h1 style="font-size:48px; color:#1a73e8; margin-bottom:0;">📈 Research Automation Engine</h1>
    <p style="font-size:18px; color:gray; margin-top:0;">
        A modern mini quant-research dashboard powered by Python signals & automated insights.
    </p>
</div>
""", unsafe_allow_html=True)


# CARD COMPONENT
def card(content):
    st.markdown(f"""
    <div style="
        background-color:#ffffff;
        padding:20px;
        border-radius:12px;
        border:1px solid #e0e0e0;
        box-shadow:0px 2px 8px rgba(0,0,0,0.06);
        margin-bottom:20px;">
        {content}
    </div>
    """, unsafe_allow_html=True)



# INPUT

ticker = st.text_input("Enter Ticker Symbol", "AAPL").upper()

run_btn = st.button("Run Analysis", use_container_width=True)



# MAIN LOGIC
if run_btn:
    with st.spinner("Fetching data..."):
        df = load_data(ticker)
        spy = yf.download("SPY", period="1y", progress=False)

    raw = compute_all_signals(df, spy)
    norm = normalize_dict(raw)

    # Prepare Close Series for sparkline
    price_series = df["Close"]
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.squeeze("columns")
    prices = price_series.tail(60).tolist()

  
    # PRICE TREND SECTION
    st.subheader("📉 Price Trend (Last 60 Days)")

    card(f"<pre style='font-size:20px;'>{sparkline(prices)}</pre>")

  
    # PRICE CHART SECTION
    st.subheader("📊 Price Chart (1Y)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=price_series,
        mode="lines",
        name=ticker,
        line=dict(color="#1a73e8", width=2)
    ))
    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


    # COLUMNS FOR SIGNAL TABLES
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📘 Raw Quant Signals")
        df_raw = pd.DataFrame.from_dict(raw, orient="index", columns=["Value"])
        card(df_raw.to_html(),)

    with col2:
        st.subheader("📗 Normalized Signals (0–1 scale)")
        df_norm = pd.DataFrame.from_dict(norm, orient="index", columns=["Normalized"])
        card(df_norm.to_html(),)


    # SUMMARY
    st.subheader("📝 Research Summary")
    summary_html = summarize_signals(ticker, raw, norm).replace("\n", "<br>")
    card(f"<p style='font-size:17px;'>{summary_html}</p>")


# END OF FILE
