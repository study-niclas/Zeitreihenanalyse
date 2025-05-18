import ruptures as rpt
import pandas as pd
import matplotlib.pyplot as plt

class BreakpointDetector:
    def __init__(self, model="rbf", penalty_value=10):
        self.model = model
        self.penalty_value = penalty_value

    def detect_breakpoints(self, series):
        """Führt Breakpoint Detection durch und gibt Indizes der Breakpoints zurück."""
        data = series.values.reshape(-1, 1)
        algo = rpt.Pelt(model=self.model).fit(data)
        breakpoints = algo.predict(pen=self.penalty_value)
        return breakpoints[:-1]  # letztes Element ist Länge der Serie → entfernen

    def annotate_series(self, series):
        """Gibt DataFrame mit Breakpoints-Annotation zurück + Breakpoint-Indexliste"""
        breakpoints = self.detect_breakpoints(series)
        df = series.to_frame(name="Close")
        df["is_breakpoint"] = False
        df.loc[df.index[breakpoints], "is_breakpoint"] = True
        return df, breakpoints

    def segment_series(self, series):
        """Segmentiert Serie anhand erkannter Breakpoints → gibt Liste von Teil-Serien zurück"""
        _, breakpoints = self.annotate_series(series)
        segments = []
        prev = 0
        for bp in breakpoints:
            segment = series.iloc[prev:bp]
            if not segment.empty:
                segments.append(segment)
            prev = bp
        final_segment = series.iloc[prev:]
        if not final_segment.empty:
            segments.append(final_segment)
        return segments

    def plot_breakpoints(self, series, breakpoints, title=None):
        """
        Plottet die Zeitreihe mit vertikalen Linien an den Breakpoints.
        """
        if isinstance(series, pd.Series):
            values = series.values
            dates = series.index
        elif isinstance(series, pd.DataFrame) and "value" in series.columns:
            values = series["value"].values
            dates = series.index
        else:
            raise ValueError("Unbekanntes Datenformat für series.")

        plt.figure(figsize=(12, 6))
        plt.plot(dates, values, label='Kursverlauf', color='blue')

        # Breakpoints als vertikale Linien
        for bp in breakpoints:
            if 0 <= bp < len(dates):
                plt.axvline(x=dates[bp], color='red', linestyle='--', linewidth=1.5)

        plt.title(title or "Zeitreihe mit Breakpoints")
        plt.xlabel("Datum")
        plt.ylabel("Kurs")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
