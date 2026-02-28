# -*- coding: utf-8 -*-
import streamlit as st
from data_collector import get_stock_data, get_fundamentals
from indicators import add_indicators
from scoring import calculate_score
from backtester import backtest
from scanner import run_scanner

st.set_page_config(page_title="SwingTrade Radar B3", layout="wide")
st.title("📊 SwingTrade Radar B3")
st.markdown("Sistema de análise técnica e fundamentalista para ações brasileiras")
st.markdown("---")

# === ANÁLISE INDIVIDUAL ===
st.header("🔍 Análise Individual")
ticker = st.text_input("Digite o código da ação (ex: PETR4.SA):", value="PETR4.SA")

if st.button("Analisar Ação"):
    if not ticker:
        st.warning("Digite um código de ação")
    else:
        if not ticker.endswith(".SA"):
            ticker = ticker + ".SA"
        
        with st.spinner(f"Baixando dados de {ticker}..."):
            try:
                df = get_stock_data(ticker)
                
                if df is None or df.empty:
                    st.error(f"❌ Não foi possível baixar dados de {ticker}")
                    st.stop()
                
                fundamentals = get_fundamentals(ticker)
                df = add_indicators(df)
                score = calculate_score(df, fundamentals)
                metrics = backtest(df)
                
                preco = fundamentals.get("price") if fundamentals and fundamentals.get("price") else df["Close"].iloc[-1]
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Preço Atual", f"R$ {preco:.2f}")
                col2.metric("Score", f"{score}/100")
                col3.metric("Retorno Backtest", f"{metrics['retorno']}%")
                col4.metric("Sharpe Ratio", metrics['sharpe'])
                
                # Fundamentos
                if fundamentals and len(fundamentals) > 0:
                    st.subheader("📈 Fundamentos")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        pvp = fundamentals.get("pvp")
                        st.write(f"**P/VPL:** {pvp if pvp else 'N/A'}")
                    with col2:
                        pl = fundamentals.get("pl")
                        st.write(f"**P/L:** {pl if pl else 'N/A'}")
                    with col3:
                        roe = fundamentals.get("roe")
                        st.write(f"**ROE:** {f'{roe:.2%}' if roe else 'N/A'}")
                
                # Gráfico
                st.subheader("📊 Evolução do Preço")
                chart_data = df[["Close", "EMA9", "EMA21"]].tail(100)
                st.line_chart(chart_data)
                
                # Recomendação
                st.subheader("💡 Recomendação")
                if score >= 70:
                    st.success("🟢 **FORTE COMPRA** - Score elevado")
                elif score >= 50:
                    st.info("🟡 **COMPRA** - Score moderado")
                elif score >= 30:
                    st.warning("🟠 **NEUTRO** - Aguardar melhor ponto")
                else:
                    st.error("🔴 **VENDA/EVITAR** - Score baixo")
                
            except Exception as e:
                st.error(f"❌ Erro na análise: {str(e)}")
                st.info("Dica: Verifique se o código da ação está correto (ex: PETR4.SA)")

st.markdown("---")

# === SCANNER AUTOMÁTICO ===
st.header("🚀 Scanner Automático - Top 10")
st.info("⚠️ O scanner pode levar até 60 segundos para processar")

if st.button("Rodar Scanner Completo"):
    with st.spinner("Escaneando mercado..."):
        try:
            ranking = run_scanner(max_results=10)
            
            if "Mensagem" in ranking.columns:
                st.warning(ranking["Mensagem"].iloc[0])
            else:
                st.success(f"✅ {len(ranking)} ações encontradas!")
                st.dataframe(ranking, use_container_width=True)
                
                st.subheader("📊 Distribuição de Scores")
                if len(ranking) > 0:
                    st.bar_chart(ranking.set_index("Ticker")["Score"])
        except Exception as e:
            st.error(f"❌ Erro no scanner: {str(e)}")
            st.info("Dica: Tente rodar novamente. A API do Yahoo pode estar instável.")
