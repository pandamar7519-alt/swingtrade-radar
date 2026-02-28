# -*- coding: utf-8 -*-

def calculate_score(df, fundamentals=None):
    """
    Calcula score de 0 a 100 com detalhamento
    Retorna: (score, detalhes)
    """
    score = 50  # Score base
    detalhes = []
    detalhes.append({"Item": "Score Base", "Pontos": "+50", "Status": "➖"})
    
    try:
        # === ANÁLISE TÉCNICA (30 pontos) ===
        if "EMA9" in df.columns and "EMA21" in df.columns:
            ema9 = df["EMA9"].iloc[-1]
            ema21 = df["EMA21"].iloc[-1]
            
            if ema9 > ema21:
                score += 30
                detalhes.append({
                    "Item": f"EMA9 ({ema9:.2f}) > EMA21 ({ema21:.2f})",
                    "Pontos": "+30",
                    "Status": "✅"
                })
            else:
                score -= 20
                detalhes.append({
                    "Item": f"EMA9 ({ema9:.2f}) < EMA21 ({ema21:.2f})",
                    "Pontos": "-20",
                    "Status": "❌"
                })
        
        # === RSI (20 pontos) ===
        if "RSI" in df.columns:
            rsi = df["RSI"].iloc[-1]
            if 40 < rsi < 60:
                score += 20
                detalhes.append({
                    "Item": f"RSI = {rsi:.1f} (Zona neutra)",
                    "Pontos": "+20",
                    "Status": "✅"
                })
            elif 30 <= rsi <= 40:
                score += 15
                detalhes.append({
                    "Item": f"RSI = {rsi:.1f} (Levemente sobrevendido)",
                    "Pontos": "+15",
                    "Status": "✅"
                })
            elif rsi < 30:
                score += 10
                detalhes.append({
                    "Item": f"RSI = {rsi:.1f} (Sobrevendido)",
                    "Pontos": "+10",
                    "Status": "⚠️"
                })
            elif rsi > 70:
                score -= 10
                detalhes.append({
                    "Item": f"RSI = {rsi:.1f} (Sobrecomprado)",
                    "Pontos": "-10",
                    "Status": "❌"
                })
            else:
                detalhes.append({
                    "Item": f"RSI = {rsi:.1f} (Neutro)",
                    "Pontos": "+0",
                    "Status": "➖"
                })
        
        # === ANÁLISE FUNDAMENTALISTA (20 pontos) ===
        if fundamentals and len(fundamentals) > 0:
            pvp = fundamentals.get("pvp")
            if pvp and pvp < 1.5:
                score += 20
                detalhes.append({
                    "Item": f"P/VPL = {pvp:.2f} (Muito barato)",
                    "Pontos": "+20",
                    "Status": "✅"
                })
            elif pvp and pvp < 2:
                score += 15
                detalhes.append({
                    "Item": f"P/VPL = {pvp:.2f} (Barato)",
                    "Pontos": "+15",
                    "Status": "✅"
                })
            elif pvp and pvp < 3:
                score += 5
                detalhes.append({
                    "Item": f"P/VPL = {pvp:.2f} (Justo)",
                    "Pontos": "+5",
                    "Status": "➖"
                })
            elif pvp:
                detalhes.append({
                    "Item": f"P/VPL = {pvp:.2f} (Caro)",
                    "Pontos": "+0",
                    "Status": "❌"
                })
            else:
                detalhes.append({
                    "Item": "P/VPL não disponível",
                    "Pontos": "+0",
                    "Status": "➖"
                })
        else:
            detalhes.append({
                "Item": "Fundamentos não disponíveis",
                "Pontos": "+0",
                "Status": "➖"
            })
        
        # Limita score entre 0 e 100
        score_final = max(0, min(100, score))
        
        return score_final, detalhes
        
    except Exception as e:
        print(f"Erro no cálculo do score: {e}")
        return 50, [{"Item": "Erro no cálculo", "Pontos": "0", "Status": "❌"}]
