import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class OutlierDetector:
    def __init__(self, window=10, zscore_threshold=4, iqr_multiplier=2, mad_threshold=4):
        self.window = window
        self.zscore_threshold = zscore_threshold
        self.iqr_multiplier = iqr_multiplier
        self.mad_threshold = mad_threshold

    def detect_outliers_zscore(self, series):
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]

        outliers = pd.Series(False, index=series.index)

        for i in range(len(series)):
            start_idx = max(0, i - self.window)
            window_data = series.iloc[start_idx:i]

            if len(window_data) > 0:
                mean = window_data.mean()
                std = window_data.std()

                # Sicherstellen, dass std ein Skalar und nicht NaN ist
                if pd.api.types.is_scalar(std) and pd.notna(std) and std > 0:
                    z_score = (series.iloc[i] - mean) / std
                    outliers.iloc[i] = abs(z_score) > self.zscore_threshold
                else:
                    outliers.iloc[i] = False
            else:
                outliers.iloc[i] = False

        return outliers

    def detect_outliers_iqr(self, series):
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]

        outliers = pd.Series(False, index=series.index)

        for i in range(len(series)):
            start_idx = max(0, i - self.window)
            window_data = series.iloc[start_idx:i]

            if len(window_data) > 0:
                q1 = window_data.quantile(0.25)
                q3 = window_data.quantile(0.75)
                iqr = q3 - q1

                lower_bound = q1 - self.iqr_multiplier * iqr
                upper_bound = q3 + self.iqr_multiplier * iqr

                outliers.iloc[i] = (series.iloc[i] < lower_bound) or (series.iloc[i] > upper_bound)
            else:
                outliers.iloc[i] = False

        return outliers

    def detect_outliers_mad(self, series):
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]

        outliers = pd.Series(False, index=series.index)

        for i in range(len(series)):
            start_idx = max(0, i - self.window)
            window_data = series.iloc[start_idx:i]

            if len(window_data) > 0:
                median = window_data.median()
                mad = np.median(np.abs(window_data - median))

                if pd.api.types.is_scalar(mad) and pd.notna(mad) and mad > 0:
                    deviation = abs(series.iloc[i] - median) / mad
                    outliers.iloc[i] = deviation > self.mad_threshold
                else:
                    outliers.iloc[i] = False
            else:
                outliers.iloc[i] = False

        return outliers

    def _detect_outliers(self, series):
        outliers_zscore = self.detect_outliers_zscore(series)
        outliers_iqr = self.detect_outliers_iqr(series)
        outliers_mad = self.detect_outliers_mad(series)

        # Kombiniere: Ein Ausreißer ist, wenn mindestens zwei Methoden zustimmen
        combined = (outliers_zscore & outliers_iqr) | (outliers_zscore & outliers_mad) | (outliers_iqr & outliers_mad)
        return combined

    def replace_outliers_with_mean(self, series, outliers):
        series_copy = series.copy()
        outlier_idx = outliers[outliers].index

        for idx in outlier_idx:
            pos = series.index.get_loc(idx)
            start_idx = max(0, pos - self.window)
            if pos > 0:
                series_copy.loc[idx] = series.iloc[start_idx:pos].mean()
            else:
                # Wenn kein vorheriger Wert vorhanden, einfach Originalwert lassen
                series_copy.loc[idx] = series.loc[idx]

        return series_copy

    def process_series(self, series, plot=False):
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]

        outliers = self._detect_outliers(series)
        cleaned = self.replace_outliers_with_mean(series, outliers)

        if plot:
            plt.figure(figsize=(12, 6))
            plt.plot(series.index, series, label='Original')
            plt.scatter(series.index[outliers], series[outliers], color='red', label='Ausreißer')
            #plt.plot(series.index, cleaned, label='Bereinigt')
            plt.legend()
            plt.title('Ausreißererkennung und Bereinigung')
            plt.xlabel('Datum')
            plt.ylabel('Kurs')
            plt.grid(True)
            plt.show()

        return cleaned

    def process_dict(self, data_dict, plot=False):
        cleaned_dict = {}
        for name, series in data_dict.items():
            print(f"Verarbeite {name}...")
            cleaned_dict[name] = self.process_series(series, plot=plot)
        return cleaned_dict
