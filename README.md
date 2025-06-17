
# 📈 Technical Strategy Backtesting Framework

This project implements a modular backtesting and optimization pipeline for technical trading strategies using the [`backtesting.py`](https://kernc.github.io/backtesting.py/) library. It enables comparative analysis across multiple assets and strategies, emphasizing robust parameter tuning and out-of-sample evaluation.

## 🧠 Overview

We analyze two commonly used strategies in technical analysis:

- **SMA Cross (Simple Moving Average Crossover)** — A trend-following strategy.
- **RSI (Relative Strength Index)** — A momentum oscillator.

These are applied to real financial data from Yahoo Finance, split chronologically into train/test sets. The strategies are optimized using **Return [%]** and then backtested on the test set to evaluate performance.

---

## 🧪 Experiment Summary

We selected two assets: **AAPL** and **AMZN**, each with at least 2 years of historical daily and 4h data.

### 📌 Key Steps

1. **Data Loading**: Downloaded from Yahoo Finance using `yfinance`.
2. **Train/Test Split**: Chronological 70% (train) / 30% (test).
3. **Optimization**: Grid search on hyperparameters for each strategy using Return [%].
4. **Backtesting**: Simulation on test data to measure realistic performance.
5. **Comparison**: Each strategy is benchmarked against Buy & Hold.

---

## 📊 Results Format (Review actual results on report.ipynb)

### 🔹 AAPL

| Strategy    | Return [%] | Sharpe Ratio | Win Rate |
|-------------|------------|---------------|----------|
| SMA Cross   | XX.XX      | X.XX          | XX.X%    |
| RSI         | XX.XX      | X.XX          | XX.X%    |
| Buy & Hold  | XX.XX      | X.XX          | —        |

### 🔹 AMZN

| Strategy    | Return [%] | Sharpe Ratio | Win Rate |
|-------------|------------|---------------|----------|
| SMA Cross   | XX.XX      | X.XX          | XX.X%    |
| RSI         | XX.XX      | X.XX          | XX.X%    |
| Buy & Hold  | XX.XX      | X.XX          | —        |

> 🔎 **Observation**: While SMA Cross captured trending periods better in AAPL, RSI showed stronger results in AMZN, especially during range-bound conditions.

---

## 🗂️ Project Structure

technical_analysis/

├── tech_analysis/

│ ├── init.py

│ ├── main.py # Entry point for running full experiment

│ ├── strategies.py # SMA and RSI strategy classes

│ ├── optimization.py # Grid search logic for SMA and RSI

│ ├── train_test_split.py # Historical data split with yfinance

│ └── utils.py 

├── report.ipynb

├── README.md

└── requirements.txt

## ⚙️ How to Run

### 🔧 Install dependencies

```
pip install -r requirements.txt
```

## 🚀 Run Experiment

You can run the full optimization + backtesting pipeline by executing:

```
from tech_analysis.main import main

results = main(tickers=['AAPL', 'AMZN'], console_print=True)
```

This will:

Fetch the data

Split it into train/test

Optimize parameters for each strategy

Backtest on test set

Return a dictionary with results per asset

## 📓 View Results in Jupyter

Navigate to the report/ folder and open the notebook:

```
jupyter notebook report.ipynb
```
>>>>>>> 6cbb73d (Initial commit)
