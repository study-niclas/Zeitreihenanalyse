import yfinance as yf
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

ticker = yf.Ticker("MBG.DE")
df = ticker.history(period="10y")  # 10 Jahre Rückblick


y = df['Close'].dropna()
y.plot(title="Mercedes-Benz")
plt.ylabel("EUR")
plt.show()




