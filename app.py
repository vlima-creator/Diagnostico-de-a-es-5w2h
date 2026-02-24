"""
Aplicação Streamlit para Diagnóstico de Ações 5W2H.

Este aplicativo permite que consultores preencham ações durante reuniões de start
com clientes, aplicando a metodologia 5W2H, calculando scores e gerando relatórios.
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from utils.calculadora import Calculadora5W2H
from utils.relatorio import GeradorRelatorio


# Configuração da página
st.set_page_config(
    page_title="Diagnóstico 5W2H",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado (simplificado para evitar conflitos de renderização)
st.markdown("""
    <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if "plano" not in st.session_state:
    st.session_state.plano = []

if "metricas" not in st.session_state:
    st.session_state.metricas = {}

# Carregar banco de ações
@st.cache_resource
def carregar_acoes():
    """Carrega o banco de ações do arquivo JSON."""
    with open("data/acoes.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Inicializar calculadora e gerador de relatórios
calculadora = Calculadora5W2H()
gerador_relatorio = GeradorRelatorio()

# Carregar dados
dados = carregar_acoes()
acoes_banco = dados["acoes"]
config = dados["config"]

# Atualizar pesos da calculadora
calculadora.peso_impacto = config["peso_impacto"]
calculadora.peso_esforco = config["peso_esforco"]

# Header
st.title("📋 Diagnóstico de Ações 5W2H")
st.markdown("Ferramenta para planejamento de ações em reuniões de start com clientes")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    cliente = st.text_input(
        "Nome do Cliente",
        placeholder="Digite o nome do cliente",
        key="cliente_input"
    )
    
    data_reuniao = st.date_input(
        "Data da Reunião",
        value=datetime.now()
    )
    
    st.divider()
    st.subheader("Pesos de Cálculo")
    col1, col2 = st.columns(2)
    with col1:
        peso_impacto = st.number_input(
            "Peso Impacto",
            value=config["peso_impacto"],
            min_value=1,
            max_value=20
        )
    with col2:
        peso_esforco = st.number_input(
            "Peso Esforço",
            value=config["peso_esforco"],
            min_value=1,
            max_value=10
        )
    
    if peso_impacto != config["peso_impacto"] or peso_esforco != config["peso_esforco"]:
        calculadora.peso_impacto = peso_impacto
        calculadora.peso_esforco = peso_esforco

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Captura de Ações",
    "📊 Plano 5W2H",
    "📈 Análise",
    "📥 Relatórios"
])

# ============ TAB 1: Captura de Ações ============
with tab1:
    st.header("Captura de Ações da Reunião")
    
    if not cliente:
        st.warning("⚠️ Digite o nome do cliente na barra lateral para começar.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Seleção de ação
            acoes_nomes = [a["acao"] for a in acoes_banco]
            acao_selecionada = st.selectbox(
                "Selecione a Ação",
                acoes_nomes,
                key="acao_select"
            )
            
            # Encontrar ação no banco
            acao_template = next(
                (a for a in acoes_banco if a["acao"] == acao_selecionada),
                None
            )
            
            if acao_template:
                # Exibir informações do template
                st.markdown("### 📋 Informações da Ação")
                
                col_cat, col_imp, col_esf = st.columns(3)
                with col_cat:
                    st.metric("Categoria", acao_template["categoria"])
                with col_imp:
                    st.metric("Impacto Padrão", acao_template["impacto_padrao"])
                with col_esf:
                    st.metric("Esforço Padrão", acao_template["esforco_padrao"])
                
                # Exibir 5W2H do template
                st.markdown("### 5W2H do Template")
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("**What (O quê)?**")
                    st.write(acao_template["what"])
                    
                    st.markdown("**Why (Por quê)?**")
                    st.write(acao_template["why"])
                    
                    st.markdown("**Where (Onde)?**")
                    st.write(acao_template["where"])
                
                with col_right:
                    st.markdown("**How (Como)?**")
                    st.write(acao_template["how"])
                    
                    st.markdown("**Indicadores**")
                    st.write(acao_template["indicadores"])
        
        with col2:
            st.markdown("### 📅 Datas")
            data_inicio = st.date_input(
                "Data de Início",
                value=datetime.now(),
                key="data_inicio"
            )
            
            duracao = st.number_input(
                "Duração (dias)",
                value=acao_template["duracao_dias"] if acao_template else 7,
                min_value=1,
                max_value=90,
                key="duracao"
            )
        
        st.divider()
        
        # Customizações
        st.markdown("### 🎯 Customizações (Opcional)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            impacto_custom = st.number_input(
                "Impacto Customizado",
                value=acao_template["impacto_padrao"] if acao_template else 3,
                min_value=1,
                max_value=5,
                key="impacto_custom"
            )
        
        with col2:
            esforco_custom = st.number_input(
                "Esforço Customizado",
                value=acao_template["esforco_padrao"] if acao_template else 3,
                min_value=1,
                max_value=5,
                key="esforco_custom"
            )
        
        with col3:
            custo_custom = st.number_input(
                "Custo Customizado (R$)",
                value=acao_template["custo_padrao"] if acao_template else 0.0,
                min_value=0.0,
                step=100.0,
                key="custo_custom"
            )
        
        st.divider()
        
        # Informações adicionais
        st.markdown("### 👤 Informações Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            responsavel = st.text_input(
                "Responsável",
                placeholder="Nome do responsável",
                key="responsavel"
            )
        
        with col2:
            status = st.selectbox(
                "Status",
                ["Planejado", "Em andamento", "Concluído", "Bloqueado"],
                key="status"
            )
        
        notas = st.text_area(
            "Notas da Reunião",
            placeholder="Contexto, restrições, combinados...",
            height=100,
            key="notas"
        )
        
        st.divider()
        
        # Botão para adicionar ação
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("✅ Adicionar Ação", use_container_width=True):
                if not responsavel:
                    st.error("❌ Digite o nome do responsável!")
                else:
                    # Gerar plano 5W2H
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
                    
                    # Adicionar ao plano
                    st.session_state.plano.append(plano_acao)
                    
                    # Recalcular métricas
                    st.session_state.metricas = calculadora.calcular_metricas_plano(
                        st.session_state.plano
                    )
                    
                    st.success(f"✅ Ação '{acao_selecionada}' adicionada ao plano!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Limpar Plano", use_container_width=True):
                st.session_state.plano = []
                st.session_state.metricas = {}
                st.info("🔄 Plano limpo!")
                st.rerun()

# ============ TAB 2: Plano 5W2H ============
with tab2:
    st.header("Plano de Ações 5W2H")
    
    if not st.session_state.plano:
        st.info("📭 Nenhuma ação adicionada ainda. Adicione ações na aba 'Captura de Ações'.")
    else:
        # Resumo do plano
        st.markdown("### 📊 Resumo do Plano")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total de Ações",
                st.session_state.metricas.get("total_acoes", 0)
            )
        
        with col2:
            st.metric(
                "Score Total",
                f"{st.session_state.metricas.get('score_total', 0):.1f}"
            )
        
        with col3:
            st.metric(
                "Score Médio",
                f"{st.session_state.metricas.get('score_medio', 0):.1f}"
            )
        
        with col4:
            st.metric(
                "Custo Total",
                f"R$ {st.session_state.metricas.get('custo_total', 0):,.2f}"
            )
        
        with col5:
            st.metric(
                "Duração (dias)",
                st.session_state.metricas.get("duracao_total_dias", 0)
            )
        
        st.divider()
        
        # Tabela de ações
        st.markdown("### 📋 Detalhes das Ações")
        
        # Preparar dados para tabela
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
        
        st.divider()
        
        # Expandir detalhes de cada ação
        st.markdown("### 🔍 Detalhes Completos (5W2H)")
        
        for idx, acao in enumerate(st.session_state.plano, 1):
            with st.expander(f"**{idx}. {acao['acao']}** - {acao['prioridade']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**What (O quê)?**")
                    st.write(acao["what"])
                    
                    st.markdown("**Why (Por quê)?**")
                    st.write(acao["why"])
                    
                    st.markdown("**Where (Onde)?**")
                    st.write(acao["where"])
                    
                    st.markdown("**Indicadores**")
                    st.write(acao["indicadores"])
                
                with col2:
                    st.markdown("**How (Como)?**")
                    st.write(acao["how"])
                    
                    st.markdown("**Informações**")
                    info_cols = st.columns(2)
                    with info_cols[0]:
                        st.write(f"**Responsável:** {acao['responsavel']}")
                        st.write(f"**Início:** {acao['data_inicio'].strftime('%d/%m/%Y')}")
                        st.write(f"**Fim:** {acao['data_fim'].strftime('%d/%m/%Y')}")
                        st.write(f"**Duração:** {acao['duracao_dias']} dias")
                    
                    with info_cols[1]:
                        st.write(f"**Custo:** R$ {acao['custo']:,.2f}")
                        st.write(f"**Impacto:** {acao['impacto']}/5")
                        st.write(f"**Esforço:** {acao['esforco']}/5")
                        st.write(f"**Score:** {acao['score']:.1f}")
                    
                    if acao["notas"]:
                        st.markdown("**Notas**")
                        st.write(acao["notas"])
                
                # Botão para remover ação
                col_remove = st.columns([1, 4])[0]
                with col_remove:
                    if st.button(f"🗑️ Remover", key=f"remove_{idx}", use_container_width=True):
                        st.session_state.plano.pop(idx - 1)
                        st.session_state.metricas = calculadora.calcular_metricas_plano(
                            st.session_state.plano
                        )
                        st.success("✅ Ação removida!")
                        st.rerun()

# ============ TAB 3: Análise ============
with tab3:
    st.header("Análise do Plano")
    
    if not st.session_state.plano:
        st.info("📭 Nenhuma ação adicionada ainda.")
    else:
        # Distribuição por categoria
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📂 Distribuição por Categoria")
            
            categoria_data = st.session_state.metricas.get("acoes_por_categoria", {})
            if categoria_data:
                df_categoria = pd.DataFrame(
                    list(categoria_data.items()),
                    columns=["Categoria", "Quantidade"]
                )
                st.bar_chart(df_categoria.set_index("Categoria"))
        
        with col2:
            st.markdown("### 🎯 Distribuição por Prioridade")
            
            prioridade_data = st.session_state.metricas.get("acoes_por_prioridade", {})
            if prioridade_data:
                df_prioridade = pd.DataFrame(
                    list(prioridade_data.items()),
                    columns=["Prioridade", "Quantidade"]
                )
                st.bar_chart(df_prioridade.set_index("Prioridade"))
        
        st.divider()
        
        # Timeline de Gantt simplificada
        st.markdown("### 📅 Timeline das Ações")
        
        timeline = calculadora.calcular_timeline_gantt(st.session_state.plano)
        
        df_timeline = pd.DataFrame([
            {
                "Ação": a["acao"],
                "Início": a["data_inicio"],
                "Fim": a["data_fim"],
                "Duração": a["duracao_dias"]
            }
            for a in timeline
        ])
        
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Análise de score
        st.markdown("### 📊 Análise de Score")
        
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
        
        # Gráfico de scores
        df_scores = pd.DataFrame([
            {
                "Ação": a["acao"][:30] + "..." if len(a["acao"]) > 30 else a["acao"],
                "Score": a["score"]
            }
            for a in st.session_state.plano
        ])
        
        st.bar_chart(df_scores.set_index("Ação"))

# ============ TAB 4: Relatórios ============
with tab4:
    st.header("Geração de Relatórios")
    
    if not st.session_state.plano:
        st.info("📭 Nenhuma ação adicionada ainda.")
    else:
        if not cliente:
            st.warning("⚠️ Digite o nome do cliente na barra lateral para gerar relatórios.")
        else:
            st.markdown("### 📥 Baixar Relatórios")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gerar PDF
                pdf_bytes = gerador_relatorio.gerar_pdf(
                    cliente=cliente,
                    acoes=st.session_state.plano,
                    metricas=st.session_state.metricas,
                    data_reuniao=datetime.combine(data_reuniao, datetime.min.time())
                )
                
                st.download_button(
                    label="📄 Baixar PDF",
                    data=pdf_bytes,
                    file_name=f"Plano_5W2H_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            with col2:
                # Gerar Excel
                excel_bytes = gerador_relatorio.gerar_excel(
                    cliente=cliente,
                    acoes=st.session_state.plano,
                    metricas=st.session_state.metricas
                )
                
                st.download_button(
                    label="📊 Baixar Excel",
                    data=excel_bytes,
                    file_name=f"Plano_5W2H_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            st.divider()
            
            st.markdown("### 📋 Pré-visualização do Relatório")
            
            # Mostrar resumo
            st.markdown("#### Resumo Executivo")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total de Ações",
                    st.session_state.metricas.get("total_acoes", 0)
                )
            
            with col2:
                st.metric(
                    "Score Total",
                    f"{st.session_state.metricas.get('score_total', 0):.1f}"
                )
            
            with col3:
                st.metric(
                    "Custo Total",
                    f"R$ {st.session_state.metricas.get('custo_total', 0):,.2f}"
                )
            
            st.divider()
            
            # Tabela de ações para relatório
            st.markdown("#### Ações do Plano")
            
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

# Footer
st.divider()
st.markdown("---")
st.markdown("**Diagnóstico de Ações 5W2H** | Versão 1.0")
st.markdown("Ferramenta para planejamento estratégico em reuniões de start com clientes")
