import streamlit as st
from data_collector import get_stock_data, get_fundamentals
from indicators import add_indicators
from scoring import calculate_score
from backtester import backtest

st.title("📊 SwingTrade Radar B3")

ticker = st.text_input("Digite o código da ação (ex: PETR4):")

if st.button("Analisar"):
    df = get_stock_data(ticker)
    fundamentals = get_fundamentals(ticker)

    if fundamentals["price"] and fundamentals["price"] < 20:
        df = add_indicators(df)
        score = calculate_score(df, fundamentals)
        retorno = backtest(df)

        st.write(f"Preço Atual: R$ {fundamentals['price']}")
        st.write(f"Score: {score}/75")
        st.write(f"Backtest Retorno: {retorno}%")

        if score >= 55:
            st.success("🟢 Potencialmente interessante para Swing Trade")
        else:
            st.warning("🔴 Baixa pontuação para Swing Trade")
    else:
        st.error("Ação acima de R$20 ou sem dados.")