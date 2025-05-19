
from modular_data_read import TickerDataManager
from outlier_detection import OutlierDetector
from breakpoint_detection import BreakpointDetector
from stationarity import StationarityTransformer

type = "normalized" 
data_dict = {}


manager = TickerDataManager()
manager.data_read("MBG.DE")
manager.data_read("TSLA")

normalized_data_dict = {ticker: data[type] for ticker, data in manager.ticker_dict.items()}

detector = OutlierDetector(window=10)
cleaned_dict = detector.process_dict(normalized_data_dict, plot=True)


# Breakpoint-Detektor
bp_detector = BreakpointDetector(penalty_value=10)



for ticker in manager.ticker_dict.keys():
    raw = manager.ticker_dict[ticker]
    cleaned = cleaned_dict[ticker]
    
    # Breakpoint-Analyse
    annotated_df, breakpoints = bp_detector.annotate_series(cleaned)
    segments = bp_detector.segment_series(cleaned)

    # Zusammensetzen
    data_dict[ticker] = {
        type : raw,
        "cleaned": cleaned,
        "breakpoints": breakpoints,
        "annotated": annotated_df,
        "segments": segments
    }

# Ausgabe zur Kontrolle
for ticker, info in data_dict.items():
    print(f"{ticker}: {len(info['segments'])} Segmente, {len(info['breakpoints'])} Breakpoints")





transformer = StationarityTransformer()

# 1. Beste Transformationseinstellungen finden
best_params = transformer.find_best_transformation(data_dict, key='cleaned')

print("Beste Transformationseinstellungen:")
print(f"Log-Transformation: {best_params['log_transform']}")
print(f"Differenzierungsgrad: {best_params['diff_order']}")
print(f"Mittlerer ADF p-Wert: {best_params['mean_adf_pvalue']:.4f}")
print(f"Mittlerer KPSS p-Wert: {best_params['mean_kpss_pvalue']:.4f}")

# 2. Transformer konfigurieren
transformer.log_transform = best_params['log_transform']
transformer.diff_order = best_params['diff_order']

# 3. Transformation durchführen und Ergebnisse holen
transformed_dict, stationarity_results = transformer.process_dict(data_dict, key='cleaned', test=True)

# 4. Ergebnisse ins data_dict speichern
for ticker in transformed_dict:
    if ticker not in data_dict:
        data_dict[ticker] = {}
    data_dict[ticker]['transformed'] = transformed_dict[ticker]
    data_dict[ticker]['stationarity_results'] = stationarity_results[ticker]

# 5. PACF-Plot für transformierte Zeitreihen
transformed_data_wrapped = {k: {'cleaned': v} for k, v in transformed_dict.items()}
transformer.plot_pacf_stocks(transformed_data_wrapped)
