"""Shared helper: data loading."""
import os
import pandas as pd


def load_data(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="gbk")
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    if ext == ".sav":
        import pyreadstat
        df, _ = pyreadstat.read_sav(path)
        return df
    if ext == ".dta":
        return pd.read_stata(path)
    raise ValueError(f"Unsupported file type: {ext} (use csv/xlsx/sav/dta)")
