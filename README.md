# Research Automation Engine (RAE)

A beginner-friendly quant research project inspired by automated workflows used in modern AI-driven platforms like **Boosted.ai Alfa**.

This project fetches stock data, computes basic quant signals, normalizes them, and produces a clean, natural-language research summary—without any machine learning.

---
<h2 align="center">🌐 Live Demo</h2>

<p align="center">
  <a href="https://research-automation-engine.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Launch%20App-Click%20Here-blue?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

<p align="center">
  Try the fully interactive dashboard here:<br>
  <strong>https://research-automation-engine.streamlit.app/</strong>
</p>

<hr>

## 🚀 What This Project Does

Given a ticker:

python research.py AAPL

yaml
Copy code

The engine automatically:

1. Downloads 1 year of OHLCV data  
2. Computes 7 quant signals  
3. Normalizes the signals  
4. Prints a clean table  
5. Generates a simple research summary  

---

## 📊 Signals Included

| Signal | Meaning |
|--------|---------|
| **1M Return** | Short-term momentum |
| **3M Return** | Mid-term trend |
| **6M Return** | Long-term momentum |
| **30D Volatility** | Recent risk |
| **Volume Trend** | Buying/selling interest |
| **Beta vs SPY** | Market sensitivity |
| **60D Sharpe Ratio** | Risk-adjusted performance |

These are the real metrics analysts use.

---

## 🧠 Why This Matters (Beginner Friendly)

Quant funds and research teams automate workflows like:

- Data ingestion  
- Signal computation  
- Preliminary analysis  
- Report generation  

This project is a tiny version of that workflow.

---

## 🏗 Folder Structure

research-automation-engine/
│
├── data_ingest.py
├── signals.py
├── report.py
├── research.py
├── requirements.txt
└── README.md

yaml
Copy code

---

## 📦 Installation

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

yaml
Copy code

---

## ▶️ Run

python research.py MSFT
python research.py NFLX
python research.py TSLA

yaml
Copy code

---

## 📈 Sample Output

=== SIGNAL TABLE ===
| 3M_Return_% | 7.84 | 0.75 |
...

=== SUMMARY ===
📈 Research Summary for AAPL
• Positive 3M momentum...
• Volatility is moderate...

yaml
Copy code

---

## 🔧 How to Extend the Project

- Add PE ratio, PB, or fundamentals  
- Add sector comparison  
- Add simple moving averages (SMA20, SMA50)  
- Export the report to PDF  
- Build a Streamlit dashboard  
- Build an API endpoint  
- Add multiprocessing ingestion  

---

## 📝 Notes for Recruiters

This project demonstrates:

- Python engineering  
- Modularity  
- Clean finance logic  
- CLI interface design  
- Research automation concepts  

Perfect for someone new to quant + tech.

---