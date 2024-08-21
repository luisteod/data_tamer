import pandas as pd
import unidecode

def normalize_column(series):
    series_cp = series.copy()
    series_cp = series_cp.fillna("")

    def normalize_text(text):
        text = text.lower()
        text = unidecode.unidecode(text)
        text = text.strip()
        text = " ".join(text.split())  # Remove espaços extras
        return text

    series_cp = series_cp.apply(normalize_text)

    return series_cp