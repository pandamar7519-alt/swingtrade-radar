# -*- coding: utf-8 -*-
import streamlit as st

# Apenas imports no topo - NENHUM processamento aqui
st.set_page_config(page_title="SwingTrade Radar", layout="wide")
st.title("📊 SwingTrade Radar B3")

# Mensagem de boas-vindas
st.success("✅ Aplicativo carregado com sucesso!")
st.info("👈 Use o menu lateral para navegar")

# Menu lateral
st.sidebar.header("Menu")
opcao = st.sidebar.radio("Escolha:", ["Análise Individual", "Scanner"])

# === ANÁLISE INDIVIDUAL ===
if opcao == "Análise Individual":
    st.header("🔍 Análise Individual")
    ticker = st.text_input("Código da ação (ex: PETR4.SA):", value="PETR4.SA")
    
    if st.button("Analisar"):
        if ticker:
            with st.spinner(f"Processando {ticker}..."):
                try:
                    from data_collector import get_stock_data, get_fundamentals
                    from indicators import add_indicators
                    from scoring import calculate_score
                    
                    if not ticker.endswith(".SA"):
                        ticker = ticker + ".SA"
                    
                    df = get_stock_data(ticker)
                    
                    if df is None or df.empty:
                        st.error(f"❌ Não foi possível carregar {ticker}")
                    else:
                        fundamentals = get_fundamentals(ticker)
                        df = add_indicators(df)
                        score = calculate_score(df, fundamentals)
                        
                        col1, col2 = st.columns(2)
                        col1.metric("Preço", f"R$ {df['Close'].iloc[-1]:.2f}")
                        col2.metric("Score", f"{score}/100")
                        
                        st.line_chart(df[["Close"]].tail(60))
                        
                        if score >= 70:
                            st.success("🟢 Forte Compra")
                        elif score >= 50:
                            st.info("🟡 Compra Moderada")
                        else:
                            st.warning("🔴 Evitar")
                            
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        else:
            st.warning("Digite um código")

# === SCANNER ===
elif opcao == "Scanner":
    st.header("🚀 Scanner de Ações")
    st.info("⚠️ Pode levar até 60 segundos")
    
    if st.button("Iniciar Scanner"):
        with st.spinner("Escaneando..."):
            try:
                from scanner import run_scanner
                resultado = run_scanner(max_results=10)
                
                if "Mensagem" in resultado.columns:
                    st.warning(resultado["Mensagem"].iloc[0])
                else:
                    st.success(f"✅ {len(resultado)} ações encontradas!")
                    st.dataframe(resultado, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Erro no scanner: {str(e)}")
