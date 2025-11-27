import numpy as np
import pandas as pd

def to_float(x):
    """Converts Series/numpy scalars to Python float safely."""
    if hasattr(x, "iloc"):
        try:
            return float(x.iloc[0])
        except:
            return float(x.mean()) if hasattr(x, "mean") else np.nan
    try:
        return float(x)
    except:
        return np.nan


def compute_returns(df: pd.DataFrame, days: int) -> float:
    """
    Computes percent return over a given number of days.
    """
    if len(df) < days:
        return np.nan
    return to_float((df["Close"].iloc[-1] / df["Close"].iloc[-days] - 1) * 100)



def compute_volatility(df: pd.DataFrame, days: int = 30) -> float:
    """
    Computes rolling volatility (standard deviation of daily returns * sqrt(252)).
    """
    if len(df) < days:
        return np.nan
    daily_ret = df["Close"].pct_change().dropna()
    return to_float(np.std(daily_ret[-days:]) * np.sqrt(252))



def compute_volume_trend(df: pd.DataFrame, days: int = 30) -> float:
    """
    % change in avg volume for the last N days vs the previous N days.
    """
    if len(df) < days * 2:
        return np.nan

    recent = df["Volume"].iloc[-days:].mean()
    prev = df["Volume"].iloc[-2*days:-days].mean()

    return to_float((recent / prev - 1) * 100)



def compute_beta(df: pd.DataFrame, benchmark_df: pd.DataFrame) -> float:
    stock_ret = df["Close"].pct_change().dropna()
    bench_ret = benchmark_df["Close"].pct_change().dropna()

    min_len = min(len(stock_ret), len(bench_ret))
    if min_len < 30:
        return np.nan

    stock_ret = stock_ret[-min_len:]
    bench_ret = bench_ret[-min_len:]

    # Convert to numpy arrays
    s = stock_ret.to_numpy()
    b = bench_ret.to_numpy()

    if len(s) < 2 or len(b) < 2:
        return np.nan

    cov = np.cov(s, b)[0, 1]
    var = np.var(b)

    return to_float(cov / var) if var != 0 else np.nan





def compute_sharpe(df: pd.DataFrame, window: int = 60) -> float:
    daily_ret = df["Close"].pct_change().dropna()

    if len(daily_ret) < window:
        return np.nan

    window_ret = daily_ret[-window:]
    mean = float(window_ret.mean() * 252)
    std = float(window_ret.std() * np.sqrt(252))

    if std == 0:
        return np.nan

    return to_float(mean / std)





def compute_all_signals(df: pd.DataFrame, benchmark_df: pd.DataFrame) -> dict:
    return {
        "1M_Return_%": compute_returns(df, 21),
        "3M_Return_%": compute_returns(df, 63),
        "6M_Return_%": compute_returns(df, 126),
        "30D_Volatility_%": compute_volatility(df),
        "Volume_Trend_%": compute_volume_trend(df),
        "Beta_vs_SPY": compute_beta(df, benchmark_df),
        "Sharpe_60D": compute_sharpe(df)
    }
