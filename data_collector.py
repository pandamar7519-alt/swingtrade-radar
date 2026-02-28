import yfinance as yf
import pandas as pd


def get_stock_data(ticker):

    try:
        df = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            return None

        # Normaliza MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Padroniza nomes
        df.columns = [col.capitalize() for col in df.columns]

        # Garante que Close exista
        if "Close" not in df.columns:
            if "Adj close" in df.columns:
                df["Close"] = df["Adj close"]
            else:
                return None

        df = df.dropna()

        return df

    except Exception:
        return None

