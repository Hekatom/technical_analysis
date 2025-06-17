from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import warnings
warnings.simplefilter("ignore")

try:
    from tech_analysis.utils import compute_rsi
    print("Ejecutado desde JN")
except:
    from utils import compute_rsi
    print("Ejecutado desde main/consola")



class SmaCross(Strategy):
    """
    Estrategia de medias moviles simples
    """
    n1 = 5
    n2 = 13

    # Definir Parametros
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    #Definir Estrategia
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()



class RSIStrategy(Strategy):
    """
    Estrategia basada en RSI:
    - Compra cuando RSI cruza arriba de 'oversold'.
    - Cierra la posición cuando RSI cruza abajo de 'overbought'.
    """
    period = 14
    oversold = 30
    overbought = 70

    def init(self):
        # self.rsi será un array con los valores de RSI
        self.rsi = self.I(compute_rsi, self.data.Close, self.period)

    def next(self):

        #print(f"RSI actual: {self.rsi[-1]}")

        if self.rsi[-1] < self.oversold:
            self.buy()
        elif self.rsi[-1] > self.overbought:
            self.position.close()
        