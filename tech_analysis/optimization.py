from backtesting import Backtest
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")

class SMAOptTechAnalysis:

    def __init__(self, Strategy):
        self.strategy = Strategy

    def sma_params_n_tf_optimization(self, set_type, data, n1, n2):
        bt = Backtest(data, self.strategy, cash=10_000_000, commission=0.002)

        stats, heatmap = bt.optimize(
        # Definimos parametros a optimizar
        n1=n1,
        n2=n2,
        constraint= lambda p: p.n1 < p.n2,
        maximize='Return [%]', # Podemos usar las metricas de rendimiento de stats 
        return_heatmap=True)

        best_params = heatmap.sort_values(ascending=False)
        best_results = {'interval':set_type, 'n1': best_params.index[0][0],
                        'n2': best_params.index[0][1], 'Return [%]': best_params.iloc[0],
                        'No. of Trades': stats['# Trades']}
        return best_results
    
    
    def sma_strategy_optimization(self, all_data, n1, n2):
        train_results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                train_results.append(self.sma_params_n_tf_optimization(set_type, df, n1, n2))
        optimal_tf_df = pd.DataFrame(train_results)
        return optimal_tf_df.sort_values(by='Return [%]', ascending=False)

        

class RSIOptTechAnalysis:
    def __init__(self, Strategy):
        self.strategy = Strategy

    def rsi_param_optimization(self, set_type, data, period_range, oversold_range, overbought_range):
        bt = Backtest(data, self.strategy, cash=10_000_000, commission=0.002)
        stats, heatmap = bt.optimize(
            period=period_range,
            oversold=oversold_range,
            overbought=overbought_range,
            constraint=lambda p: p.oversold < p.overbought,
            maximize='Return [%]',    # o 'Sharpe Ratio'
            return_heatmap=True
        )
        # Sacamos los mejores parámetros
        best = heatmap.sort_values(ascending=False).iloc[0]
        return {
             'interval': set_type,
             'period': heatmap.name[0],
             'oversold': heatmap[heatmap == best].index.get_level_values('oversold')[0],
             'overbought': heatmap[heatmap == best].index.get_level_values('overbought')[0],
             'Return [%]': best
        }

    def rsi_strategy_optimization(self, all_data, period_range, oversold_range, overbought_range):
        results = []
        # print('results:', results)
        for set_type, df in all_data.items():
            # print('cuenta', set_type, df)
            if 'train' in set_type:
                # print('hubo train')
                results.append(
                    self.rsi_param_optimization(set_type, df, period_range, oversold_range, overbought_range)
                )
        # print('results:', results[1])
        # print('results:')
        # print(results)

        # Devuelve un DataFrame ordenado
        return pd.DataFrame(results)