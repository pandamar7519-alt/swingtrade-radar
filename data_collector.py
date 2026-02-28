def get_stock_data(ticker):

    import yfinance as yf
    import pandas as pd

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

        # Remove MultiIndex se existir
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Padroniza nomes das colunas
        df.columns = [col.capitalize() for col in df.columns]

        # Garante que exista coluna Close
        if "Close" not in df.columns:
            return None

        # Converte tudo para número (evita erro str - str)
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        return df

    except Exception:
        return None
