import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

ticker = yf.Ticker("MBG.DE")

# Hole historische Daten manuell
df = ticker.history(period="10y")  # 10 Jahre Rückblick

y = df['Close'].dropna()


y.plot(title="Mercedes-Benz")
plt.ylabel("EUR")
plt.show()


p_value = adfuller(y)[1]
print(p_value)
differentiation_order = 0
while p_value > 0.05:  # Solange die Zeitreihe nicht stationär ist
    # Erste Differenzierung durchführen
    y = y.diff().dropna()
    differentiation_order += 1
    p_value= adfuller(y)[1]
    print(f"{differentiation_order}: {p_value} ")


# Beispiel: Log-Transformation + Differenzierung
y_log = np.log(y)
y_stationary = y_log.diff().dropna()

# Plot der transformierten Zeitreihe
y_stationary.plot(title='Transformierte Zeitreihe (Log + 1. Differenz)', figsize=(10, 5))
plt.grid(True)
plt.show()
