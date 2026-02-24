import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Diagnóstico 5W2H", layout="wide")

# Carregar ações
try:
    with open("data/acoes.json", encoding="utf-8") as f:
        dados = json.load(f)
    acoes_banco = dados.get("acoes", [])
    config = dados.get("config", {"peso_impacto": 10, "peso_esforco": 2})
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Session state
if "plano" not in st.session_state:
    st.session_state.plano = []

st.title("📋 Diagnóstico de Ações 5W2H")
st.write("Ferramenta para planejamento estratégico em reuniões de start com clientes")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    cliente = st.text_input("Nome do Cliente", placeholder="Digite o cliente")
    data_reuniao = st.date_input("Data da Reunião")
    
    if st.button("🗑️ Limpar Plano"):
        st.session_state.plano = []
        st.rerun()

# Abas
tab1, tab2, tab3 = st.tabs(["📝 Captura", "📊 Plano", "📈 Análise"])

# ============ TAB 1: CAPTURA ============
with tab1:
    st.header("Captura de Ações")
    
    if not cliente:
        st.warning("⚠️ Digite o nome do cliente na barra lateral para começar")
    elif not acoes_banco:
        st.error("❌ Nenhuma ação disponível no banco de dados")
    else:
        # Seleção de ação
        acao_nomes = [a.get("acao", f"Ação {a.get('id')}") for a in acoes_banco]
        acao_nome = st.selectbox("Selecione a Ação", acao_nomes)
        
        # Encontrar ação selecionada
        acao = next((a for a in acoes_banco if a.get("acao") == acao_nome), None)
        
        if acao:
            # Exibir informações da ação
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📂 Categoria", acao.get("categoria", "N/A"))
            with col2:
                st.metric("⚡ Impacto Padrão", acao.get("impacto_padrao", 0))
            with col3:
                st.metric("💪 Esforço Padrão", acao.get("esforco_padrao", 0))
            
            st.markdown("---")
            
            # Detalhes 5W2H
            st.subheader("5W2H da Ação")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**What (O quê)?**\n{acao.get('what', 'N/A')}")
                st.write(f"**Why (Por quê)?**\n{acao.get('why', 'N/A')}")
                st.write(f"**Where (Onde)?**\n{acao.get('where', 'N/A')}")
            
            with col2:
                st.write(f"**How (Como)?**\n{acao.get('how', 'N/A')}")
                st.write(f"**Indicadores**\n{acao.get('indicadores', 'N/A')}")
            
            st.markdown("---")
            
            # Formulário de customização
            st.subheader("Customizar Ação")
            
            col1, col2 = st.columns(2)
            
            with col1:
                data_inicio = st.date_input("Data de Início", value=datetime.now().date(), key="data_inicio_key")
                duracao = st.number_input(
                    "Duração (dias)", 
                    value=acao.get("duracao_dias", 7), 
                    min_value=1, 
                    max_value=180
                )
                impacto = st.number_input(
                    "Impacto (1-5)", 
                    value=acao.get("impacto_padrao", 3), 
                    min_value=1, 
                    max_value=5
                )
            
            with col2:
                esforco = st.number_input(
                    "Esforço (1-5)", 
                    value=acao.get("esforco_padrao", 3), 
                    min_value=1, 
                    max_value=5
                )
                responsavel = st.text_input("Responsável", placeholder="Nome da pessoa")
                status = st.selectbox("Status", ["Planejado", "Em andamento", "Concluído"])
            
            notas = st.text_area("Notas da Reunião", placeholder="Contexto, restrições, combinados...")
            
            # Botão adicionar
            if st.button("✅ Adicionar Ação", use_container_width=True):
                if not responsavel.strip():
                    st.error("❌ Digite o nome do responsável!")
                else:
                    # Calcular score
                    score = (impacto * config.get("peso_impacto", 10)) - (esforco * config.get("peso_esforco", 2))
                    
                    # Calcular data fim
                    data_fim = datetime.combine(data_inicio, datetime.min.time()) + timedelta(days=duracao)
                    
                    # Determinar prioridade
                    if score >= 30:
                        prioridade = "P0 - Crítica"
                    elif score >= 20:
                        prioridade = "P1 - Alta"
                    elif score >= 10:
                        prioridade = "P2 - Média"
                    elif score >= 0:
                        prioridade = "P3 - Baixa"
                    else:
                        prioridade = "P4 - Muito Baixa"
                    
                    # Adicionar ao plano
                    st.session_state.plano.append({
                        "acao": acao_nome,
                        "categoria": acao.get("categoria", ""),
                        "responsavel": responsavel.strip(),
                        "data_inicio": data_inicio,
                        "data_fim": data_fim.date(),
                        "duracao": duracao,
                        "impacto": impacto,
                        "esforco": esforco,
                        "score": score,
                        "prioridade": prioridade,
                        "status": status,
                        "notas": notas,
                        "what": acao.get("what", ""),
                        "why": acao.get("why", ""),
                        "where": acao.get("where", ""),
                        "how": acao.get("how", ""),
                        "indicadores": acao.get("indicadores", "")
                    })
                    
                    st.success(f"✅ Ação '{acao_nome}' adicionada ao plano!")
                    st.rerun()

# ============ TAB 2: PLANO ============
with tab2:
    st.header("Plano 5W2H")
    
    if not st.session_state.plano:
        st.info("ℹ️ Nenhuma ação adicionada ainda. Comece na aba 'Captura'")
    else:
        # Métricas
        total_acoes = len(st.session_state.plano)
        score_total = sum(a["score"] for a in st.session_state.plano)
        score_medio = score_total / total_acoes if total_acoes > 0 else 0
        impacto_total = sum(a["impacto"] for a in st.session_state.plano)
        esforco_total = sum(a["esforco"] for a in st.session_state.plano)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total", total_acoes)
        with col2:
            st.metric("Score Total", f"{score_total:.1f}")
        with col3:
            st.metric("Score Médio", f"{score_medio:.1f}")
        with col4:
            st.metric("Impacto Total", impacto_total)
        with col5:
            st.metric("Esforço Total", esforco_total)
        
        st.markdown("---")
        
        # Tabela de ações
        st.subheader("Tabela de Ações")
        
        df_data = []
        for idx, acao in enumerate(st.session_state.plano):
            df_data.append({
                "ID": idx + 1,
                "Ação": acao["acao"],
                "Categoria": acao["categoria"],
                "Responsável": acao["responsavel"],
                "Início": acao["data_inicio"],
                "Fim": acao["data_fim"],
                "Dias": acao["duracao"],
                "Impacto": acao["impacto"],
                "Esforço": acao["esforco"],
                "Score": f"{acao['score']:.1f}",
                "Prioridade": acao["prioridade"],
                "Status": acao["status"]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Detalhes Completos")
        
        for idx, acao in enumerate(st.session_state.plano):
            with st.expander(f"🔍 {idx + 1}. {acao['acao']} - {acao['prioridade']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Categoria:** {acao['categoria']}")
                    st.write(f"**Responsável:** {acao['responsavel']}")
                    st.write(f"**Início:** {acao['data_inicio']}")
                    st.write(f"**Fim:** {acao['data_fim']}")
                    st.write(f"**Duração:** {acao['duracao']} dias")
                
                with col2:
                    st.write(f"**Impacto:** {acao['impacto']}/5")
                    st.write(f"**Esforço:** {acao['esforco']}/5")
                    st.write(f"**Score:** {acao['score']:.1f}")
                    st.write(f"**Status:** {acao['status']}")
                    st.write(f"**Prioridade:** {acao['prioridade']}")
                
                st.write("**What (O quê)?**")
                st.write(acao["what"])
                
                st.write("**Why (Por quê)?**")
                st.write(acao["why"])
                
                st.write("**Where (Onde)?**")
                st.write(acao["where"])
                
                st.write("**How (Como)?**")
                st.write(acao["how"])
                
                st.write("**Indicadores**")
                st.write(acao["indicadores"])
                
                if acao["notas"]:
                    st.write("**Notas**")
                    st.write(acao["notas"])
                
                if st.button(f"🗑️ Remover", key=f"remove_{idx}"):
                    st.session_state.plano.pop(idx)
                    st.rerun()

# ============ TAB 3: ANÁLISE ============
with tab3:
    st.header("Análise do Plano")
    
    if not st.session_state.plano:
        st.info("ℹ️ Nenhuma ação adicionada ainda")
    else:
        # Distribuição por categoria
        st.subheader("Distribuição por Categoria")
        cat_count = {}
        for a in st.session_state.plano:
            cat = a["categoria"]
            cat_count[cat] = cat_count.get(cat, 0) + 1
        
        if cat_count:
            df_cat = pd.DataFrame(list(cat_count.items()), columns=["Categoria", "Quantidade"])
            st.bar_chart(df_cat.set_index("Categoria"))
        
        st.markdown("---")
        
        # Distribuição por prioridade
        st.subheader("Distribuição por Prioridade")
        pri_count = {}
        for a in st.session_state.plano:
            pri = a["prioridade"]
            pri_count[pri] = pri_count.get(pri, 0) + 1
        
        if pri_count:
            df_pri = pd.DataFrame(list(pri_count.items()), columns=["Prioridade", "Quantidade"])
            st.bar_chart(df_pri.set_index("Prioridade"))
        
        st.markdown("---")
        
        # Análise de scores
        st.subheader("Análise de Scores")
        scores = [a["score"] for a in st.session_state.plano]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Score Máximo", f"{max(scores):.1f}")
        with col2:
            st.metric("Score Mínimo", f"{min(scores):.1f}")
        with col3:
            st.metric("Score Médio", f"{sum(scores)/len(scores):.1f}")
        with col4:
            st.metric("Score Total", f"{sum(scores):.1f}")
        
        st.markdown("---")
        
        # Gráfico de scores
        st.subheader("Scores por Ação")
        df_scores = pd.DataFrame([{
            "Ação": a["acao"][:25] + "..." if len(a["acao"]) > 25 else a["acao"],
            "Score": a["score"]
        } for a in st.session_state.plano])
        st.bar_chart(df_scores.set_index("Ação"))

# Footer
st.markdown("---")
st.markdown("**Diagnóstico de Ações 5W2H** v1.0 | Ferramenta para planejamento estratégico")
