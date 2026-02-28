# -*- coding: utf-8 -*-
import streamlit as st
from data_collector import get_stock_data, get_fundamentals  # ✅ Adicionado get_fundamentals
from indicators import add_indicators
from scoring import calculate_score
from backtester import backtest
from scanner import run_scanner

st.set_page_config(page_title="SwingTrade Radar B3", layout="wide")
st.title("📊 SwingTrade Radar B3")

# === ANÁLISE INDIVIDUAL ===
st.header("🔍 Análise Individual")
ticker = st.text_input("Digite o código da ação (ex: PETR4.SA):", value="PETR4.SA")

if st.button("Analisar Ação"):
    if not ticker.endswith(".SA"):
        ticker += ".SA"  # ✅ Garante sufixo brasileiro
        
    with st.spinner(f"Baixando dados de {ticker}..."):
        try:
            df = get_stock_data(ticker)
            
            if df is None or df.empty:
                st.error(f"❌ Não foi possível baixar dados de {ticker}")
                st.stop()
            
            fundamentals = get_fundamentals(ticker)
            df = add_indicators(df)
            score = calculate_score(df, fundamentals)
            
            preco = fundamentals.get("price") or df["Close"].iloc[-1]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Preço", f"R$ {preco:.2f}")
            col2.metric("Score", f"{score}/100")
            
            if score >= 70:
                col3.success("🟢 Forte Compra")
            elif score >= 50:
                col3.info("🟡 Compra Moderada")
            else:
                col3.error("🔴 Evitar")
            
            # Gráfico simples
            st.line_chart(df[["Close", "EMA9", "EMA21"]].tail(60))
            
        except Exception as e:
            st.error(f"Erro na análise: {str(e)}")

st.markdown("---")

# === SCANNER AUTOMÁTICO ===
st.header("🚀 Scanner Automático")
st.info("⚠️ Pode levar até 60 segundos para processar todas as ações")

if st.button("Rodar Scanner (Top 10)"):
    with st.spinner("Escaneando mercado..."):
        try:
            # ✅ Passa max_results=10 para evitar timeout
            ranking = run_scanner(max_results=10)
            
            if "Mensagem" in ranking.columns:
                st.warning(ranking["Mensagem"].iloc[0])
            else:
                st.success(f"✅ {len(ranking)} ações encontradas!")
                st.dataframe(ranking, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no scanner: {str(e)}")
            st.info("Dica: Tente rodar novamente. A API do Yahoo pode estar instável.")
