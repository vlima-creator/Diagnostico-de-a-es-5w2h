import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="5W2H", layout="wide")

# Carregar ações
with open("data/acoes.json") as f:
    dados = json.load(f)

acoes_banco = dados["acoes"]
config = dados["config"]

# Session state
if "plano" not in st.session_state:
    st.session_state.plano = []

st.title("Diagnóstico 5W2H")

# Sidebar
with st.sidebar:
    st.header("Configuração")
    cliente = st.text_input("Cliente")
    data_reuniao = st.date_input("Data")

# Abas
tab1, tab2, tab3 = st.tabs(["Captura", "Plano", "Análise"])

with tab1:
    st.header("Captura de Ações")
    
    if not cliente:
        st.info("Digite o cliente na barra lateral")
    else:
        acao_nome = st.selectbox("Ação", [a["acao"] for a in acoes_banco])
        acao = next(a for a in acoes_banco if a["acao"] == acao_nome)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Categoria", acao["categoria"])
        col2.metric("Impacto", acao["impacto_padrao"])
        col3.metric("Esforço", acao["esforco_padrao"])
        
        st.write(f"**What:** {acao['what']}")
        st.write(f"**Why:** {acao['why']}")
        st.write(f"**Where:** {acao['where']}")
        st.write(f"**How:** {acao['how']}")
        st.write(f"**Indicadores:** {acao['indicadores']}")
        
        data_inicio = st.date_input("Início", key="data_inicio")
        duracao = st.number_input("Duração (dias)", value=acao["duracao_dias"], min_value=1, max_value=90)
        impacto = st.number_input("Impacto", value=acao["impacto_padrao"], min_value=1, max_value=5)
        esforco = st.number_input("Esforço", value=acao["esforco_padrao"], min_value=1, max_value=5)
        responsavel = st.text_input("Responsável")
        notas = st.text_area("Notas")
        
        if st.button("Adicionar"):
            if responsavel:
                score = (impacto * config["peso_impacto"]) - (esforco * config["peso_esforco"])
                data_fim = datetime(data_inicio.year, data_inicio.month, data_inicio.day) + pd.Timedelta(days=duracao)
                
                st.session_state.plano.append({
                    "acao": acao_nome,
                    "categoria": acao["categoria"],
                    "responsavel": responsavel,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim.date(),
                    "duracao": duracao,
                    "impacto": impacto,
                    "esforco": esforco,
                    "score": score,
                    "notas": notas,
                    "what": acao["what"],
                    "why": acao["why"],
                    "where": acao["where"],
                    "how": acao["how"]
                })
                st.success("Ação adicionada!")
                st.rerun()
            else:
                st.error("Digite o responsável")

with tab2:
    st.header("Plano 5W2H")
    
    if not st.session_state.plano:
        st.info("Nenhuma ação adicionada")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", len(st.session_state.plano))
        col2.metric("Score Total", round(sum(a["score"] for a in st.session_state.plano), 1))
        col3.metric("Impacto", sum(a["impacto"] for a in st.session_state.plano))
        col4.metric("Esforço", sum(a["esforco"] for a in st.session_state.plano))
        
        df = pd.DataFrame([{
            "Ação": a["acao"],
            "Categoria": a["categoria"],
            "Responsável": a["responsavel"],
            "Início": a["data_inicio"],
            "Fim": a["data_fim"],
            "Impacto": a["impacto"],
            "Esforço": a["esforco"],
            "Score": round(a["score"], 1)
        } for a in st.session_state.plano])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.write("---")
        for i, acao in enumerate(st.session_state.plano):
            st.write(f"**{i+1}. {acao['acao']}**")
            st.write(f"What: {acao['what']}")
            st.write(f"Why: {acao['why']}")
            st.write(f"Where: {acao['where']}")
            st.write(f"How: {acao['how']}")
            st.write(f"Responsável: {acao['responsavel']}")
            
            if st.button(f"Remover {i+1}", key=f"rem_{i}"):
                st.session_state.plano.pop(i)
                st.rerun()
            st.write("---")

with tab3:
    st.header("Análise")
    
    if st.session_state.plano:
        cat_count = {}
        for a in st.session_state.plano:
            cat = a["categoria"]
            cat_count[cat] = cat_count.get(cat, 0) + 1
        
        st.write("Distribuição por Categoria")
        st.bar_chart(pd.DataFrame(list(cat_count.items()), columns=["Categoria", "Quantidade"]).set_index("Categoria"))
        
        st.write("Scores")
        scores = [a["score"] for a in st.session_state.plano]
        col1, col2, col3 = st.columns(3)
        col1.metric("Máximo", max(scores))
        col2.metric("Mínimo", min(scores))
        col3.metric("Médio", round(sum(scores)/len(scores), 1))
        
        st.write("Gráfico de Scores")
        st.bar_chart(pd.DataFrame([{
            "Ação": a["acao"][:20],
            "Score": a["score"]
        } for a in st.session_state.plano]).set_index("Ação"))
    else:
        st.info("Nenhuma ação adicionada")

st.write("---")
st.write("Diagnóstico 5W2H v1.0")
