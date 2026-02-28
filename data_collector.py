import yfinance as yf
import pandas as pd


def get_stock_data(ticker):

    try:
        df = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            progress=False
        )

        if df.empty:
            return None

        # Se vier MultiIndex, normaliza
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.dropna()

        return df

    except Exception:
        return None

