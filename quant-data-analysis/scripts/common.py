"""Shared helpers: data loading and small formatting utilities."""
import sys, os
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


def fmt_p(p):
    if p is None or pd.isna(p):
        return "NA"
    return "< .001" if p < .001 else "= " + f"{p:.3f}".lstrip("0")


def fmt_num(x, d=2):
    if x is None or pd.isna(x):
        return "NA"
    return f"{x:.{d}f}"
