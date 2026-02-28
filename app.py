# -*- coding: utf-8 -*-
import streamlit as st
import datetime

st.set_page_config(page_title="SwingTrade Radar B3", layout="wide")
st.title("📊 SwingTrade Radar B3")
st.caption(f"Última atualização: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.markdown("---")

# Mensagem de boas-vindas
st.success("✅ Aplicativo carregado com sucesso!")

# Menu lateral
st.sidebar.header("Menu")
opcao = st.sidebar.radio("Escolha:", ["Análise Individual", "Scanner"])
st.sidebar.markdown("---")
st.sidebar.caption("📊 Dados: Yahoo Finance")

# === ANÁLISE INDIVIDUAL ===
if opcao == "Análise Individual":
    st.header("🔍 Análise Individual Detalhada")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("Código da ação (ex: PETR4.SA):", value="PETR4.SA")
    with col2:
        mostrar_detalhes = st.checkbox("Mostrar detalhamento do score", value=True)
    
    if st.button("Analisar Ação"):
        if not ticker:
            st.warning("⚠️ Digite um código de ação")
        else:
            if not ticker.endswith(".SA"):
                ticker = ticker + ".SA"
            
            with st.spinner(f"🔄 Processando {ticker}..."):
                try:
                    from data_collector import get_stock_data, get_fundamentals
                    from indicators import add_indicators
                    from scoring import calculate_score
                    
                    df = get_stock_data(ticker)
                    
                    if df is None or df.empty:
                        st.error(f"❌ Não foi possível carregar dados de {ticker}")
                        st.info("💡 Verifique se o código está correto (ex: PETR4.SA)")
                    else:
                        fundamentals = get_fundamentals(ticker)
                        df = add_indicators(df)
                        score, detalhes = calculate_score(df, fundamentals)
                        
                        # Métricas principais
                        col1, col2, col3 = st.columns(3)
                        col1.metric("💰 Preço Atual", f"R$ {df['Close'].iloc[-1]:.2f}")
                        col2.metric("📈 Score", f"{score}/100")
                        
                        # Recomendação
                        if score >= 70:
                            recomendacao = "🟢 FORTE COMPRA"
                            col3.success(recomendacao)
                        elif score >= 55:
                            recomendacao = "🟡 COMPRA MODERADA"
                            col3.info(recomendacao)
                        elif score >= 40:
                            recomendacao = "⚪ NEUTRO"
                            col3.warning(recomendacao)
                        else:
                            recomendacao = "🔴 EVITAR/VENDER"
                            col3.error(recomendacao)
                        
                        # === DETALHAMENTO DO SCORE ===
                        if mostrar_detalhes:
                            st.markdown("---")
                            st.subheader("📋 Detalhamento do Score")
                            
                            # Tabela de detalhamento
                            detalhes_df = []
                            for d in detalhes:
                                detalhes_df.append({
                                    "Critério": d["Item"],
                                    "Pontuação": d["Pontos"],
                                    "Status": d["Status"]
                                })
                            
                            st.table(detalhes_df)
                            
                            # Resumo
                            st.info(f"""
                            **💡 Interpretação:**
                            
                            O score de **{score}/100** foi calculado com base em:
                            - ✅ **Análise Técnica**: Tendência das médias móveis (EMA9 vs EMA21)
                            - ✅ **Momentum**: RSI (Índice de Força Relativa)
                            - ✅ **Fundamentos**: P/VPL (Preço sobre Valor Patrimonial)
                            
                            **Recomendação:** {recomendacao}
                            """)
                        
                        # Gráfico
                        st.markdown("---")
                        st.subheader("📊 Evolução do Preço")
                        
                        if "EMA9" in df.columns and "EMA21" in df.columns:
                            chart_data = df[["Close", "EMA9", "EMA21"]].tail(60)
                            st.line_chart(chart_data)
                        else:
                            st.line_chart(df[["Close"]].tail(60))
                        
                        # Fundamentos
                        if fundamentals and len(fundamentals) > 0:
                            st.markdown("---")
                            st.subheader("📈 Dados Fundamentalistas")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                pvp = fundamentals.get("pvp")
                                st.write(f"**P/VPL:** {pvp:.2f}" if pvp else "**P/VPL:** N/A")
                            with col2:
                                pl = fundamentals.get("pl")
                                st.write(f"**P/L:** {pl:.2f}" if pl else "**P/L:** N/A")
                            with col3:
                                roe = fundamentals.get("roe")
                                st.write(f"**ROE:** {roe:.2%}" if roe else "**ROE:** N/A")
                            
                except Exception as e:
                    st.error(f"❌ Erro na análise: {str(e)}")
                    st.info("💡 Dica: Tente novamente em alguns instantes")

# === SCANNER ===
elif opcao == "Scanner":
    st.header("🚀 Scanner de Ações")
    st.info("⚠️ O scanner analisa 10 ações e pode levar até 60 segundos")
    
    if st.button("Iniciar Scanner"):
        with st.spinner("🔄 Escaneando mercado..."):
            try:
                from scanner import run_scanner
                resultado = run_scanner(max_results=10)
                
                if "Mensagem" in resultado.columns:
                    st.warning(resultado["Mensagem"].iloc[0])
                else:
                    st.success(f"✅ {len(resultado)} ações encontradas!")
                    st.dataframe(resultado, use_container_width=True)
                    
                    # Gráfico de scores
                    if len(resultado) > 0:
                        st.subheader("📊 Distribuição de Scores")
                        st.bar_chart(resultado.set_index("Ticker")["Score"])
                    
                    # Legenda
                    st.markdown("---")
                    st.caption("""
                    **Legenda de Scores:**
                    - 🟢 70-100: Forte Compra
                    - 🟡 55-69: Compra Moderada  
                    - ⚪ 40-54: Neutro
                    - 🔴 0-39: Evitar/Vender
                    """)
                    
            except Exception as e:
                st.error(f"❌ Erro no scanner: {str(e)}")
                st.info("💡 Dica: Tente novamente. A API do Yahoo pode estar instável.")

# Rodapé
st.markdown("---")
st.caption("📊 SwingTrade Radar B3 | Dados fornecidos por Yahoo Finance | Use com responsabilidade")
