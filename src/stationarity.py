import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_pacf
import matplotlib.pyplot as plt
import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning

class StationarityTransformer:
    def __init__(self, standardize=True):
        self.standardize = standardize
        # Am Ende gespeicherte beste Parameter:
        self.best_params = {
            'log_transform': None,
            'diff_order': None,
            'mean_adf_pvalue': None,
            'mean_kpss_pvalue': None
        }

    def test_stationarity(self, series):
        result = {}

        # ADF-Test
        adf_result = adfuller(series.dropna(), autolag='AIC')
        result['ADF Statistic'] = adf_result[0]
        result['ADF p-value'] = adf_result[1]

        # KPSS-Test
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', InterpolationWarning)
                kpss_result = kpss(series.dropna(), regression='c')
            result['KPSS Statistic'] = kpss_result[0]
            result['KPSS p-value'] = kpss_result[1]
        except:
            result['KPSS Statistic'] = np.nan
            result['KPSS p-value'] = np.nan

        return result

    def transform_series(self, series, log_transform, diff_order):
        transformed = series.copy()

        if log_transform:
            transformed = np.log(transformed)

        for _ in range(diff_order):
            transformed = transformed.diff()

        if self.standardize:
            transformed = (transformed - transformed.mean()) / transformed.std()

        return transformed.dropna()

    def find_best_transformation(self, data_dict, key='cleaned', max_diff=2):
        """
        Probiert alle Kombinationen von log_transform (True/False) und Differenzierungsgrad (0...max_diff)
        und bestimmt die beste Kombination basierend auf Mittelwert der p-Werte von ADF und KPSS über alle Zeitreihen.
        """
        best_score = None
        best_params = None

        for log_option in [False, True]:
            for diff_order in range(max_diff + 1):
                adf_pvalues = []
                kpss_pvalues = []

                for ticker, content in data_dict.items():
                    series = content[key]
                    transformed = self.transform_series(series, log_option, diff_order)
                    if len(transformed) < 3:
                        # Zu kurz für Tests, überspringen
                        continue

                    results = self.test_stationarity(transformed)
                    adf_pvalues.append(results['ADF p-value'])
                    kpss_pvalues.append(results['KPSS p-value'])

                # Mittelwerte bilden (nur gültige Werte)
                mean_adf = np.nanmean(adf_pvalues)
                mean_kpss = np.nanmean(kpss_pvalues)

                # Bewertung: ADF p-Wert soll möglichst klein sein (stationär),
                # KPSS p-Wert möglichst groß (stationär),
                # hier einfacher Score: KPSS p - ADF p (je größer, desto besser)
                score = mean_kpss - mean_adf

                if best_score is None or score > best_score:
                    best_score = score
                    best_params = {
                        'log_transform': log_option,
                        'diff_order': diff_order,
                        'mean_adf_pvalue': mean_adf,
                        'mean_kpss_pvalue': mean_kpss
                    }

        # Speichern
        self.best_params = best_params
        return best_params

    def process_dict(self, data_dict, key='cleaned', test=False):
        """
        Transformation aller Zeitreihen im Dictionary mit den besten Parametern aus find_best_transformation.
        """
        if self.best_params['log_transform'] is None or self.best_params['diff_order'] is None:
            raise RuntimeError("Bitte zuerst find_best_transformation aufrufen!")

        transformed_dict = {}
        stationarity_results = {}

        for ticker, content in data_dict.items():
            series = content[key]
            transformed = self.transform_series(
                series,
                self.best_params['log_transform'],
                self.best_params['diff_order']
            )
            transformed_dict[ticker] = transformed

            if test:
                stationarity_results[ticker] = self.test_stationarity(transformed)

        return transformed_dict, stationarity_results

    def plot_pacf_stocks(self, data_dict, lags=40, key='cleaned'):
        n = len(data_dict)
        fig, axes = plt.subplots(n, 1, figsize=(10, 4 * n), sharex=False)

        if n == 1:
            axes = [axes]

        for ax, (ticker, subdict) in zip(axes, data_dict.items()):
            try:
                series = subdict[key]
                plot_pacf(series, lags=lags, ax=ax, method="ywmle")
                ax.set_title(f"{ticker} - PACF")
            except Exception as e:
                ax.set_visible(False)
                print(f"Fehler bei {ticker}: {e}")

        plt.tight_layout()
        plt.show()
