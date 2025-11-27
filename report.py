import numpy as np
from tabulate import tabulate

def normalize_dict(d):
    """
    Min-max normalizes a dict of numeric values.
    Ensures all values are Python floats.
    """
    clean = {k: (float(v) if v is not None else np.nan) for k, v in d.items()}

    vals = [v for v in clean.values() if not np.isnan(v)]
    if not vals:
        return clean

    min_v, max_v = min(vals), max(vals)
    if min_v == max_v:
        return {k: 0.5 for k in clean}

    return {
        k: (v - min_v) / (max_v - min_v) if not np.isnan(v) else np.nan
        for k, v in clean.items()
    }




def summarize_signals(ticker, raw, norm):
    """
    Generates natural-language summary.
    """

    momentum = raw["3M_Return_%"]
    vol = raw["30D_Volatility_%"]
    vol_trend = raw["Volume_Trend_%"]
    beta = raw["Beta_vs_SPY"]
    sharpe = raw["Sharpe_60D"]

    lines = [f"📈 Research Summary for **{ticker}**"]

    # Momentum
    if momentum > 0:
        lines.append(f"• The stock shows **positive 3M momentum** ({momentum:.2f}%).")
    else:
        lines.append(f"• **Negative 3M momentum** ({momentum:.2f}%), indicating weakness.")

    # Volatility
    lines.append(f"• 30-day volatility is **{vol:.2f}%**, giving a sense of recent risk.")

    # Volume
    if vol_trend > 0:
        lines.append(f"• **Volume has increased** ({vol_trend:.2f}%), suggesting stronger interest.")
    else:
        lines.append(f"• **Volume is declining** ({vol_trend:.2f}%), indicating cooling activity.")

    # Beta
    if beta > 1:
        lines.append(f"• Beta {beta:.2f} → the stock moves **more than the market**.")
    else:
        lines.append(f"• Beta {beta:.2f} → the stock is **more defensive**.")

    # Sharpe
    lines.append(f"• 60-day Sharpe ratio: **{sharpe:.2f}** (risk-adjusted strength).")

    return "\n".join(lines)


def format_table(raw, norm):
    headers = ["Signal", "Raw Value", "Normalized"]
    rows = []

    for k in raw:
        raw_val = raw[k]
        norm_val = norm[k]

        raw_str = "NaN" if np.isnan(raw_val) else f"{raw_val:.4f}"
        norm_str = "NaN" if np.isnan(norm_val) else f"{norm_val:.4f}"

        rows.append([k, raw_str, norm_str])

    return tabulate(rows, headers=headers, tablefmt="github")

def sparkline(data, bars="▁▂▃▄▅▆▇█"):
    """
    Generates an ASCII sparkline for a list of numeric values.
    """
    if len(data) == 0:
        return ""
    mn, mx = min(data), max(data)
    if mx == mn:
        return bars[0] * len(data)

    step = (mx - mn) / (len(bars) - 1)
    return "".join(bars[int((x - mn) / step)] for x in data)
