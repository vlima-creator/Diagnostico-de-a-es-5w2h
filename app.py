"""
Aplicação Streamlit para Diagnóstico de Ações 5W2H.
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime
from utils.calculadora import Calculadora5W2H
# from utils.relatorio import GeradorRelatorio  # Removido para compatibilidade

# Configuração da página
st.set_page_config(
    page_title="Diagnóstico 5W2H",
    page_icon="📋",
    layout="wide"
)

# Inicializar session state
if "plano" not in st.session_state:
    st.session_state.plano = []
if "metricas" not in st.session_state:
    st.session_state.metricas = {}

# Carregar banco de ações
@st.cache_resource
def carregar_acoes():
    with open("data/acoes.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Inicializar calculadora
calculadora = Calculadora5W2H()

# Carregar dados
dados = carregar_acoes()
acoes_banco = dados["acoes"]
config = dados["config"]

calculadora.peso_impacto = config["peso_impacto"]
calculadora.peso_esforco = config["peso_esforco"]

# Header
st.title("Diagnóstico de Ações 5W2H")
st.write("Ferramenta para planejamento de ações em reuniões de start com clientes")

# Sidebar
with st.sidebar:
    st.header("Configurações")
    cliente = st.text_input("Nome do Cliente", placeholder="Digite o nome do cliente")
    data_reuniao = st.date_input("Data da Reunião", value=datetime.now())
    
    st.write("Pesos de Cálculo")
    peso_impacto = st.number_input("Peso Impacto", value=config["peso_impacto"], min_value=1, max_value=20)
    peso_esforco = st.number_input("Peso Esforço", value=config["peso_esforco"], min_value=1, max_value=10)
    
    if peso_impacto != config["peso_impacto"] or peso_esforco != config["peso_esforco"]:
        calculadora.peso_impacto = peso_impacto
        calculadora.peso_esforco = peso_esforco

# Abas
tab1, tab2, tab3, tab4 = st.tabs(["Captura", "Plano", "Análise", "Relatórios"])

# TAB 1: Captura
with tab1:
    st.header("Captura de Ações")
    
    if not cliente:
        st.warning("Digite o nome do cliente na barra lateral")
    else:
        acoes_nomes = [a["acao"] for a in acoes_banco]
        acao_selecionada = st.selectbox("Selecione a Ação", acoes_nomes)
        
        acao_template = next((a for a in acoes_banco if a["acao"] == acao_selecionada), None)
        
        if acao_template:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Categoria", acao_template["categoria"])
            with col2:
                st.metric("Impacto", acao_template["impacto_padrao"])
            with col3:
                st.metric("Esforço", acao_template["esforco_padrao"])
            
            st.write("**What (O quê)?**")
            st.write(acao_template["what"])
            
            st.write("**Why (Por quê)?**")
            st.write(acao_template["why"])
            
            st.write("**Where (Onde)?**")
            st.write(acao_template["where"])
            
            st.write("**How (Como)?**")
            st.write(acao_template["how"])
            
            st.write("**Indicadores**")
            st.write(acao_template["indicadores"])
            
            st.write("---")
            
            data_inicio = st.date_input("Data de Início", value=datetime.now())
            duracao = st.number_input("Duração (dias)", value=acao_template["duracao_dias"], min_value=1, max_value=90)
            
            impacto_custom = st.number_input("Impacto Customizado", value=acao_template["impacto_padrao"], min_value=1, max_value=5)
            esforco_custom = st.number_input("Esforço Customizado", value=acao_template["esforco_padrao"], min_value=1, max_value=5)
            custo_custom = st.number_input("Custo Customizado (R$)", value=acao_template["custo_padrao"], min_value=0.0, step=100.0)
            
            responsavel = st.text_input("Responsável", placeholder="Nome do responsável")
            status = st.selectbox("Status", ["Planejado", "Em andamento", "Concluído", "Bloqueado"])
            notas = st.text_area("Notas da Reunião", placeholder="Contexto, restrições, combinados...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Adicionar Ação", use_container_width=True):
                    if not responsavel:
                        st.error("Digite o nome do responsável!")
                    else:
                        plano_acao = calculadora.gerar_plano_5w2h(
                            acao_template=acao_template,
                            cliente=cliente,
                            responsavel=responsavel,
                            notas=notas,
                            data_inicio=datetime.combine(data_inicio, datetime.min.time()),
                            impacto_customizado=impacto_custom,
                            esforco_customizado=esforco_custom,
                            custo_customizado=custo_custom
                        )
                        st.session_state.plano.append(plano_acao)
                        st.session_state.metricas = calculadora.calcular_metricas_plano(st.session_state.plano)
                        st.success(f"Ação '{acao_selecionada}' adicionada!")
                        st.rerun()
            
            with col2:
                if st.button("Limpar Plano", use_container_width=True):
                    st.session_state.plano = []
                    st.session_state.metricas = {}
                    st.info("Plano limpo!")
                    st.rerun()

# TAB 2: Plano
with tab2:
    st.header("Plano 5W2H")
    
    if not st.session_state.plano:
        st.info("Nenhuma ação adicionada ainda")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total", st.session_state.metricas.get("total_acoes", 0))
        with col2:
            st.metric("Score Total", f"{st.session_state.metricas.get('score_total', 0):.1f}")
        with col3:
            st.metric("Score Médio", f"{st.session_state.metricas.get('score_medio', 0):.1f}")
        with col4:
            st.metric("Custo", f"R$ {st.session_state.metricas.get('custo_total', 0):,.0f}")
        with col5:
            st.metric("Duração", f"{st.session_state.metricas.get('duracao_total_dias', 0)}d")
        
        st.write("---")
        
        dados_tabela = []
        for idx, acao in enumerate(st.session_state.plano, 1):
            dados_tabela.append({
                "ID": idx,
                "Ação": acao["acao"],
                "Categoria": acao["categoria"],
                "Responsável": acao["responsavel"],
                "Início": acao["data_inicio"].strftime("%d/%m/%Y"),
                "Fim": acao["data_fim"].strftime("%d/%m/%Y"),
                "Dias": acao["duracao_dias"],
                "Impacto": acao["impacto"],
                "Esforço": acao["esforco"],
                "Score": f"{acao['score']:.1f}",
                "Prioridade": acao["prioridade"],
                "Status": acao["status"]
            })
        
        df_tabela = pd.DataFrame(dados_tabela)
        st.dataframe(df_tabela, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("Detalhes Completos")
        
        for idx, acao in enumerate(st.session_state.plano, 1):
            st.write(f"**{idx}. {acao['acao']}** - {acao['prioridade']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**What:** " + acao["what"][:100] + "...")
                st.write("**Why:** " + acao["why"][:100] + "...")
                st.write("**Where:** " + acao["where"][:100] + "...")
            
            with col2:
                st.write(f"**Responsável:** {acao['responsavel']}")
                st.write(f"**Início:** {acao['data_inicio'].strftime('%d/%m/%Y')}")
                st.write(f"**Fim:** {acao['data_fim'].strftime('%d/%m/%Y')}")
                st.write(f"**Score:** {acao['score']:.1f}")
            
            if st.button(f"Remover ação {idx}", key=f"remove_{idx}"):
                st.session_state.plano.pop(idx - 1)
                st.session_state.metricas = calculadora.calcular_metricas_plano(st.session_state.plano)
                st.rerun()
            
            st.write("---")

# TAB 3: Análise
with tab3:
    st.header("Análise do Plano")
    
    if not st.session_state.plano:
        st.info("Nenhuma ação adicionada ainda")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Distribuição por Categoria")
            categoria_data = st.session_state.metricas.get("acoes_por_categoria", {})
            if categoria_data:
                df_categoria = pd.DataFrame(list(categoria_data.items()), columns=["Categoria", "Quantidade"])
                st.bar_chart(df_categoria.set_index("Categoria"))
        
        with col2:
            st.write("Distribuição por Prioridade")
            prioridade_data = st.session_state.metricas.get("acoes_por_prioridade", {})
            if prioridade_data:
                df_prioridade = pd.DataFrame(list(prioridade_data.items()), columns=["Prioridade", "Quantidade"])
                st.bar_chart(df_prioridade.set_index("Prioridade"))
        
        st.write("---")
        st.write("Timeline das Ações")
        timeline = calculadora.calcular_timeline_gantt(st.session_state.plano)
        df_timeline = pd.DataFrame([{
            "Ação": a["acao"],
            "Início": a["data_inicio"],
            "Fim": a["data_fim"],
            "Duração": a["duracao_dias"]
        } for a in timeline])
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("Análise de Score")
        scores = [a["score"] for a in st.session_state.plano]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Score Máximo", f"{max(scores):.1f}")
        with col2:
            st.metric("Score Mínimo", f"{min(scores):.1f}")
        with col3:
            st.metric("Score Médio", f"{sum(scores) / len(scores):.1f}")
        with col4:
            st.metric("Score Total", f"{sum(scores):.1f}")
        
        df_scores = pd.DataFrame([{
            "Ação": a["acao"][:30] + "..." if len(a["acao"]) > 30 else a["acao"],
            "Score": a["score"]
        } for a in st.session_state.plano])
        st.bar_chart(df_scores.set_index("Ação"))

# TAB 4: Relatórios
with tab4:
    st.header("Geração de Relatórios")
    
    if not st.session_state.plano:
        st.info("Nenhuma ação adicionada ainda")
    else:
        if not cliente:
            st.warning("Digite o nome do cliente na barra lateral")
        else:
            # Gerar Excel
            from utils.relatorio import GeradorRelatorio
            gerador_relatorio = GeradorRelatorio()
            
            excel_bytes = gerador_relatorio.gerar_excel(
                cliente=cliente,
                acoes=st.session_state.plano,
                metricas=st.session_state.metricas
            )
            st.download_button(
                label="Baixar Excel",
                data=excel_bytes,
                file_name=f"Plano_5W2H_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.write("---")
            st.write("Pré-visualização do Relatório")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Ações", st.session_state.metricas.get("total_acoes", 0))
            with col2:
                st.metric("Score Total", f"{st.session_state.metricas.get('score_total', 0):.1f}")
            with col3:
                st.metric("Custo Total", f"R$ {st.session_state.metricas.get('custo_total', 0):,.0f}")
            
            st.write("---")
            st.write("Ações do Plano")
            
            dados_relatorio = []
            for idx, acao in enumerate(st.session_state.plano, 1):
                dados_relatorio.append({
                    "ID": idx,
                    "Ação": acao["acao"],
                    "Categoria": acao["categoria"],
                    "Responsável": acao["responsavel"],
                    "Início": acao["data_inicio"].strftime("%d/%m/%Y"),
                    "Fim": acao["data_fim"].strftime("%d/%m/%Y"),
                    "Score": f"{acao['score']:.1f}",
                    "Prioridade": acao["prioridade"]
                })
            
            df_relatorio = pd.DataFrame(dados_relatorio)
            st.dataframe(df_relatorio, use_container_width=True, hide_index=True)

st.write("---")
st.write("Diagnóstico de Ações 5W2H | Versão 1.0")
