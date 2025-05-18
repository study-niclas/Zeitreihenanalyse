import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt

class TickerDataManager:
    def __init__(self, subfolder="data"):
        self.ticker_dict = {}
        self.subfolder = subfolder
        os.makedirs(self.subfolder, exist_ok=True)

    def get_filepath(self, share_ticker):
        return os.path.join(self.subfolder, f"{share_ticker}.csv")

    def data_read(self, share_ticker, period=10):
        filepath = self.get_filepath(share_ticker)

        if os.path.exists(filepath):
            print(f"Lese lokale Datei für {share_ticker} ein...")
            share_history = pd.read_csv(filepath, index_col=0, parse_dates=True)
        else:
            print(f"Lade Daten von yfinance für {share_ticker}...")
            share = yf.Ticker(str(share_ticker))
            period_str = str(period) + "y"
            share_history = share.history(period=period_str)['Close']
            # Direkt lokal speichern
            share_history.to_csv(filepath)

        # Speichern im internen Dictionary
        self.ticker_dict[share_ticker] = share_history

        # Plot anzeigen
        #share_history.plot(title=share_ticker)
        #plt.ylabel("EUR")
        #plt.show()

    def data_save(self, share_ticker):
        if share_ticker not in self.ticker_dict:
            raise ValueError(f"{share_ticker} nicht im Speicher vorhanden. Erst mit `.data_read(...)` laden.")
        
        filepath = self._get_filepath(share_ticker)
        self.ticker_dict[share_ticker].to_csv(filepath)
        
    def plot_all(self):

        plt.figure(figsize=(12, 6))
        for ticker, series in self.ticker_dict.items():
            plt.plot(series, label=ticker)

        plt.title("Kursverläufe aller geladenen Ticker")
        plt.xlabel("Datum")
        plt.ylabel("Kurs (EUR)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def plot_all_extended(self, ma_window=50):
        for ticker, series in self.ticker_dict.items():
            # Sicherstellen, dass wir ein DataFrame mit Spalte 'Close' haben
            if isinstance(series, pd.Series):
                df = series.to_frame(name='Close')
            else:
                df = series.copy()
            df.columns = ['Close']
            df['MA'] = df['Close'].rolling(window=ma_window).mean()
            df['Normalized'] = df['Close'] / df['Close'].iloc[0] * 100
            df['Pct Change'] = df['Close'].pct_change().cumsum() * 100  # kumulierte prozentuale Veränderung

            fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
            fig.suptitle(f"{ticker} - Kursanalyse", fontsize=14)

            # 1. Original + Moving Average
            axs[0].plot(df.index, df['Close'], label="Kurs")
            axs[0].plot(df.index, df['MA'], label=f"{ma_window}-Tage Moving Avg", linestyle='--')
            axs[0].set_ylabel("EUR")
            axs[0].legend()
            axs[0].set_title("Kurs & Gleitender Durchschnitt")

            # 2. Normalisierte Darstellung
            axs[1].plot(df.index, df['Normalized'], color='green')
            axs[1].set_ylabel("Indexiert (100)")
            axs[1].set_title("Normalisierter Kursverlauf")

            # 3. Kumulative prozentuale Veränderung
            axs[2].plot(df.index, df['Pct Change'], color='orange')
            axs[2].set_ylabel("% Veränderung")
            axs[2].set_xlabel("Datum")
            axs[2].set_title("Kumulative % Veränderung")

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.show()




