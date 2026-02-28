# -*- coding: utf-8 -*-

def calculate_score(df, fundamentals=None):
    try:
        score = 50  # Score base
        
        if "EMA9" in df.columns and "EMA21" in df.columns:
            if df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1]:
                score += 30
            else:
                score -= 20
        
        if fundamentals:
            pvp = fundamentals.get("pvp")
            if pvp and pvp < 2:
                score += 20
        
        return max(0, min(100, score))
    except:
        return 50
