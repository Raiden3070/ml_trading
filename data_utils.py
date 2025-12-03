import os
import pandas as pd
from typing import Sequence


def get_symbol_filepath(symbol: str, base_dir: str | None = None) -> str:
    base_dir = base_dir or os.path.join(os.path.dirname(__file__), "data")
    return os.path.join(base_dir, f"{symbol}_TIME_SERIES_DAILY_full.csv")


def fetch_stock_data(symbols: Sequence[str], dates: pd.DatetimeIndex, addSPY: bool = True, colname: str = "Adj Close") -> pd.DataFrame:
    symbols = list(symbols)
    if addSPY and "SPY" not in symbols:
        symbols = ["SPY"] + symbols

    df = pd.DataFrame(index=dates)
    for symbol in symbols:
        path = get_symbol_filepath(symbol)
        if not os.path.exists(path):
            continue
        data = pd.read_csv(path, index_col=0, parse_dates=True, usecols=[0, 4], na_values=['nan'])
        data = data.rename(columns={data.columns[0]: colname})
        # Align to requested dates
        data = data.reindex(dates)
        df[symbol] = data[colname]

    # Forward/back fill to handle missing values if any
    df = df.ffill().bfill()
    return df
