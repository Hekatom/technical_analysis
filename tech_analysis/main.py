import pandas as pd
from backtesting import Backtest
try:
    from train_test_split import TrainTestSets
    from strategies import SmaCross, RSIStrategy
    from optimization import SMAOptTechAnalysis, RSIOptTechAnalysis
    print("Running from console/main")
except:
    from tech_analysis.train_test_split import TrainTestSets
    from tech_analysis.strategies import SmaCross, RSIStrategy
    from tech_analysis.optimization import SMAOptTechAnalysis, RSIOptTechAnalysis
    print("Running from JN")



def load_data(ticker='AAPL', intervals=['4h', '1d'], console_print=False):
    if console_print:
        print(f"=== Loading data for {ticker} ===")
    tts = TrainTestSets()
    return tts.interval_train_test_split(ticker, intervals)


def optimize_sma(data, console_print=False):
    if console_print:
        print("=== Optimizing SMA Cross ===")
    sma_opt = SMAOptTechAnalysis(SmaCross)
    sma_results = sma_opt.sma_strategy_optimization(data, n1=range(5, 20), n2=range(20, 60))
    best = sma_results.iloc[0]
    if console_print:
        print(sma_results)
        print(f"Best SMA (\"{best.interval}\"): n1={best.n1}, n2={best.n2}, Return%={best['Return [%]']:.2f}\n")
    return sma_results, best


def optimize_rsi(data, console_print=False):
    if console_print:
        print("=== Optimizing RSI ===")
    rsi_opt = RSIOptTechAnalysis(RSIStrategy)
    rsi_results = rsi_opt.rsi_strategy_optimization(
        data,
        period_range=range(10, 31),
        oversold_range=range(20, 41, 5),
        overbought_range=range(60, 81, 5)
    )
    best = rsi_results.iloc[0]
    if console_print:
        print(rsi_results)
        print(f"Best RSI (\"{best.interval}\"): period={best.period}, oversold={best.oversold}, "
              f"overbought={best.overbought}, Return%={best['Return [%]']:.2f}\n")
    return rsi_results, best


def backtest_sma(data, best_params, console_print=False):
    if console_print:
        print("=== Backtest SMA in Test ===")
    bt = Backtest(data['1d_test'], SmaCross, cash=10_000_000, commission=0.002)
    stats = bt.run(n1=int(best_params.n1), n2=int(best_params.n2))
    if console_print:
        print(stats)
        bt.plot()
    return bt, stats


def backtest_rsi(data, best_params, console_print=False):
    if console_print:
        print("=== Backtest RSI in Test ===")
    bt = Backtest(data['1d_test'], RSIStrategy, cash=10_000_000, commission=0.002)
    stats = bt.run(
        period=int(best_params.overbought - best_params.oversold),
        oversold=int(best_params.oversold),
        overbought=int(best_params.overbought)
    )
    if console_print:
        print(stats)
        bt.plot()
    return bt, stats


def run_analysis_for_ticker(ticker, console_print=False):
    data = load_data(ticker=ticker, console_print=console_print)

    sma_results, best_sma = optimize_sma(data, console_print=console_print)
    rsi_results, best_rsi = optimize_rsi(data, console_print=console_print)

    bt_sma, stats_sma = backtest_sma(data, best_sma, console_print=console_print)
    bt_rsi, stats_rsi = backtest_rsi(data, best_rsi, console_print=console_print)

    return {
        'sma_results': sma_results,
        'rsi_results': rsi_results,
        'bt_sma': bt_sma,
        'stats_sma': stats_sma,
        'bt_rsi': bt_rsi,
        'stats_rsi': stats_rsi
    }


def main(tickers=['AAPL', 'AMZN'], console_print=True):
    results = {}
    for ticker in tickers:
        if console_print:
            print(f"\n=== Processing {ticker} ===\n")
        results[ticker] = run_analysis_for_ticker(ticker, console_print=console_print)
    return results


# Solo si se corre como script
if __name__ == '__main__':
    main(console_print=True)
