
from modular_data_read import TickerDataManager
from outlier_detection import OutlierDetector
from breakpoint_detection import BreakpointDetector

manager = TickerDataManager()
manager.data_read("MBG.DE")
manager.data_read("TSLA")

normalized_data_dict = {ticker: data["normalized"] for ticker, data in manager.ticker_dict.items()}

detector = OutlierDetector(window=10)
cleaned_dict = detector.process_dict(normalized_data_dict, plot=True)

# Strukturbrüche erkennen
bp_detector = BreakpointDetector(penalty_value=10)

for ticker, cleaned_series in cleaned_dict.items():
    annotated_df, breakpoints = bp_detector.annotate_series(cleaned_series)

    print(f"{ticker} - Breakpoints an Positionen: {breakpoints}")
    print(annotated_df[annotated_df["is_breakpoint"]])

    # Plot
    bp_detector.plot_breakpoints(cleaned_series, breakpoints, title=f"{ticker} - Breakpoint Analyse")

#TODO Daten einlesen mit yfinance
#TODO Daten bereinigen nach aussreissern und evtl. etwas glätten
#TODO Daten speichern (.csv im data ordner oder .db)
#TODO Daten splitten(80/20) für Modelltest - wie gut ist der predict
#TODO ACF and PACF https://medium.com/@kis.andras.nandor/understanding-autocorrelation-and-partial-autocorrelation-functions-acf-and-pacf-2998e7e1bcb5
#TODO Daten Visualisieren und va predict zu Relität unterschiede highlighten
#TODO https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques