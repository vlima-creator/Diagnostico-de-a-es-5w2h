import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="5W2H", layout="wide")

with open("data/acoes.json") as f:
    data = json.load(f)

if "plan" not in st.session_state:
    st.session_state.plan = []

st.title("5W2H")

with st.sidebar:
    client = st.text_input("Cliente")
    if st.button("Limpar"):
        st.session_state.plan = []
        st.rerun()

tab1, tab2, tab3 = st.tabs(["Adicionar", "Plano", "Analise"])

with tab1:
    st.header("Adicionar Acao")
    if client:
        acoes = data["acoes"]
        action_name = st.selectbox("Acao", [a["acao"] for a in acoes])
        action = next(a for a in acoes if a["acao"] == action_name)
        
        st.write(f"**What:** {action['what']}")
        st.write(f"**Why:** {action['why']}")
        st.write(f"**Where:** {action['where']}")
        st.write(f"**How:** {action['how']}")
        
        start = st.date_input("Inicio")
        duration = st.number_input("Duracao", value=7, min_value=1)
        impact = st.number_input("Impacto", value=3, min_value=1, max_value=5)
        effort = st.number_input("Esforco", value=3, min_value=1, max_value=5)
        owner = st.text_input("Responsavel")
        
        if st.button("Adicionar"):
            if owner:
                score = (impact * 10) - (effort * 2)
                end = start + timedelta(days=duration)
                st.session_state.plan.append({
                    "action": action_name,
                    "owner": owner,
                    "start": start,
                    "end": end,
                    "impact": impact,
                    "effort": effort,
                    "score": score
                })
                st.success("OK")
                st.rerun()

with tab2:
    st.header("Plano")
    if st.session_state.plan:
        for i, p in enumerate(st.session_state.plan):
            st.write(f"{i+1}. {p['action']} - Score: {p['score']}")
            st.write(f"Owner: {p['owner']} | Start: {p['start']} | End: {p['end']}")
            if st.button(f"Remove {i}", key=f"r{i}"):
                st.session_state.plan.pop(i)
                st.rerun()
    else:
        st.write("Nenhuma acao")

with tab3:
    st.header("Analise")
    if st.session_state.plan:
        scores = [p["score"] for p in st.session_state.plan]
        st.write(f"Total: {len(st.session_state.plan)}")
        st.write(f"Score Total: {sum(scores)}")
        st.write(f"Score Medio: {sum(scores)/len(scores):.1f}")
    else:
        st.write("Nenhuma acao")
