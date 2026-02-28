# -*- coding: utf-8 -*-

def calculate_score(df, fundamentals=None):
    """
    Sistema de score de 0 a 100 pontos
    """
    score = 0
    max_score = 100
    
    try:
        # Verifica colunas necessárias
        required_cols = ["EMA9", "EMA21", "RSI", "Close", "Volume"]
        for col in required_cols:
            if col not in df.columns:
                return 0
        
        # Remove NaN apenas das últimas linhas
        df = df.dropna(subset=required_cols)
        if len(df) < 30:
            return 0
        
        # === ANÁLISE TÉCNICA (70 pontos) ===
        
        # Tendência de curto prazo (20 pontos)
        if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1]:
            score += 20
        elif df["EMA9"].iloc[-1] > df["EMA21"].iloc[-2]:
            score += 10  # Cruzamento recente
        
        # Preço acima da média (15 pontos)
        if df["Close"].iloc[-1] > df["EMA21"].iloc[-1]:
            score += 15
        
        # Força da tendência (15 pontos)
        if df["EMA21"].iloc[-1] > df["EMA21"].iloc[-5]:
            score += 15  # EMA ascendente
        
        # RSI saudável (10 pontos)
        rsi = df["RSI"].iloc[-1]
        if 45 < rsi < 65:
            score += 10  # Zona neutra
        elif 30 < rsi <= 45:
            score += 5  # Levemente sobrevendido
        
        # Volume (10 pontos)
        vol_medio = df["Volume"].rolling(20).mean().iloc[-1]
        if df["Volume"].iloc[-1] > vol_medio * 1.2:
            score += 10  # Volume acima da média
        
        # === ANÁLISE FUNDAMENTISTA (30 pontos) ===
        if fundamentals:
            # PVP (10 pontos)
            if fundamentals.get("pvp") and fundamentals["pvp"] < 1.5:
                score += 10
            elif fundamentals.get("pvp") and fundamentals["pvp"] < 2:
                score += 5
            
            # PL (10 pontos)
            if fundamentals.get("pl") and fundamentals["pl"] < 10:
                score += 10
            elif fundamentals.get("pl") and fundamentals["pl"] < 15:
                score += 5
            
            # ROE (10 pontos)
            if fundamentals.get("roe") and fundamentals["roe"] > 0.15:
                score += 10
            elif fundamentals.get("roe") and fundamentals["roe"] > 0.10:
                score += 5
        
        return min(score, max_score)
        
    except Exception as e:
        print(f"Erro no cálculo do score: {e}")
        return 0
