import streamlit as st
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="5W2H", layout="wide")

# Load data
with open("acoes.json") as f:
    acoes = json.load(f)["acoes"]

config = {"peso_impacto": 10, "peso_esforco": 2}

# Session state
if "plano" not in st.session_state:
    st.session_state.plano = []

st.title("5W2H - Diagnostico")

# Sidebar
with st.sidebar:
    cliente = st.text_input("Cliente")
    if st.button("Limpar Tudo"):
        st.session_state.plano = []
        st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["Adicionar", "Visualizar", "Analise"])

# TAB 1
with tab1:
    st.header("Adicionar Acao")
    if not cliente:
        st.warning("Digite o cliente")
    else:
        acao_nome = st.selectbox("Selecione", [a["acao"] for a in acoes])
        acao = next(a for a in acoes if a["acao"] == acao_nome)
        
        st.write(f"**What:** {acao['what']}")
        st.write(f"**Why:** {acao['why']}")
        st.write(f"**Where:** {acao['where']}")
        st.write(f"**How:** {acao['how']}")
        
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("Data Inicio")
            duracao = st.number_input("Duracao (dias)", value=7, min_value=1)
            impacto = st.number_input("Impacto", value=3, min_value=1, max_value=5)
        with col2:
            esforco = st.number_input("Esforco", value=3, min_value=1, max_value=5)
            responsavel = st.text_input("Responsavel")
            status = st.selectbox("Status", ["Planejado", "Em andamento", "Concluido"])
        
        notas = st.text_area("Notas")
        
        if st.button("Adicionar Acao"):
            if responsavel:
                score = (impacto * config["peso_impacto"]) - (esforco * config["peso_esforco"])
                data_fim = datetime.combine(data_inicio, datetime.min.time()) + timedelta(days=duracao)
                
                st.session_state.plano.append({
                    "acao": acao_nome,
                    "categoria": acao["categoria"],
                    "responsavel": responsavel,
                    "data_inicio": str(data_inicio),
                    "data_fim": str(data_fim.date()),
                    "duracao": duracao,
                    "impacto": impacto,
                    "esforco": esforco,
                    "score": score,
                    "status": status,
                    "notas": notas,
                    "what": acao["what"],
                    "why": acao["why"],
                    "where": acao["where"],
                    "how": acao["how"]
                })
                st.success("Acao adicionada!")
                st.rerun()
            else:
                st.error("Digite o responsavel")

# TAB 2
with tab2:
    st.header("Plano 5W2H")
    if not st.session_state.plano:
        st.write("Nenhuma acao adicionada")
    else:
        total = len(st.session_state.plano)
        score_total = sum(a["score"] for a in st.session_state.plano)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total)
        col2.metric("Score Total", f"{score_total:.1f}")
        col3.metric("Score Medio", f"{score_total/total:.1f}")
        
        st.write("---")
        
        for i, acao in enumerate(st.session_state.plano):
            st.write(f"**{i+1}. {acao['acao']}** (Score: {acao['score']:.1f})")
            st.write(f"Categoria: {acao['categoria']}")
            st.write(f"Responsavel: {acao['responsavel']}")
            st.write(f"Inicio: {acao['data_inicio']} | Fim: {acao['data_fim']}")
            st.write(f"Impacto: {acao['impacto']}/5 | Esforco: {acao['esforco']}/5")
            st.write(f"What: {acao['what']}")
            st.write(f"Why: {acao['why']}")
            st.write(f"Where: {acao['where']}")
            st.write(f"How: {acao['how']}")
            st.write(f"Status: {acao['status']}")
            if acao['notas']:
                st.write(f"Notas: {acao['notas']}")
            
            if st.button(f"Remover {i+1}", key=f"btn_{i}"):
                st.session_state.plano.pop(i)
                st.rerun()
            
            st.write("---")

# TAB 3
with tab3:
    st.header("Analise")
    if st.session_state.plano:
        scores = [a["score"] for a in st.session_state.plano]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Max Score", f"{max(scores):.1f}")
        col2.metric("Min Score", f"{min(scores):.1f}")
        col3.metric("Avg Score", f"{sum(scores)/len(scores):.1f}")
        col4.metric("Total Impact", sum(a["impacto"] for a in st.session_state.plano))
        
        st.write("---")
        
        cat_count = {}
        for a in st.session_state.plano:
            c = a["categoria"]
            cat_count[c] = cat_count.get(c, 0) + 1
        
        st.write("Acoes por Categoria:")
        for cat, count in cat_count.items():
            st.write(f"- {cat}: {count}")
    else:
        st.write("Nenhuma acao")

st.write("---")
st.write("5W2H v1.0")
