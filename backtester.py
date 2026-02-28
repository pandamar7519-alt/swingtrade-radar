# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def backtest(df, initial_capital=10000):
    """
    Backtest com métricas completas
    """
    try:
        df = df.copy()
        
        # Sinal de compra: EMA9 > EMA21
        df["Signal"] = 0
        df.loc[df["EMA9"] > df["EMA21"], "Signal"] = 1
        
        # Retorna diários
        df["Returns"] = df["Close"].pct_change()
        
        # Estratégia (shift para evitar look-ahead bias)
        df["Strategy_Returns"] = df["Signal"].shift(1) * df["Returns"]
        
        # Remove NaN
        df = df.dropna()
        
        if len(df) == 0:
            return {"retorno": 0, "sharpe": 0, "max_drawdown": 0}
        
        # Retorno acumulado
        cumulative_return = (1 + df["Strategy_Returns"]).cumprod().iloc[-1] - 1
        
        # Sharpe Ratio (anualizado)
        sharpe = np.sqrt(252) * df["Strategy_Returns"].mean() / df["Strategy_Returns"].std() if df["Strategy_Returns"].std() != 0 else 0
        
        # Max Drawdown
        cumulative = (1 + df["Strategy_Returns"]).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # Total de trades
        trades = df["Signal"].diff().abs().sum()
        
        return {
            "retorno": round(cumulative_return * 100, 2),
            "sharpe": round(sharpe, 2),
            "max_drawdown": round(max_drawdown * 100, 2),
            "trades": int(trades)
        }
        
    except Exception as e:
        print(f"Erro no backtest: {e}")
        return {"retorno": 0, "sharpe": 0, "max_drawdown": 0, "trades": 0}
