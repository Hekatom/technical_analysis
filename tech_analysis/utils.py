import pandas as pd
import numpy as np

def compute_rsi(arr, period=14):
    arr = np.asarray(arr, dtype=float)
    delta = np.diff(arr, prepend=arr[0])

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.full_like(arr, fill_value=np.nan)
    avg_loss = np.full_like(arr, fill_value=np.nan)

    # Inicializamos la media simple para los primeros 'period' valores
    avg_gain[period] = gain[1:period+1].mean()
    avg_loss[period] = loss[1:period+1].mean()

    # Ahora el suavizado tipo Wilder
    for i in range(period+1, len(arr)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + loss[i]) / period

    rs = avg_gain / (avg_loss + 1e-10)  # evitar división por cero
    rsi = 100 - (100 / (1 + rs))

    # Los primeros period valores no tienen RSI definido
    rsi[:period] = np.nan

    return rsi
