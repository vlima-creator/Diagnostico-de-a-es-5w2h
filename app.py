import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="5W2H", layout="wide")

# Carregar dados
try:
    with open("data/acoes.json", encoding="utf-8") as f:
        dados = json.load(f)
    acoes_banco = dados.get("acoes", [])
    config = dados.get("config", {"peso_impacto": 10, "peso_esforco": 2})
except:
    st.error("Erro ao carregar dados")
    st.stop()

# Session state
if "plano" not in st.session_state:
    st.session_state.plano = []

st.title("5W2H - Diagnóstico de Ações")

# Sidebar
with st.sidebar:
    st.header("Configuração")
    cliente = st.text_input("Cliente")
    data_reuniao = st.date_input("Data")
    if st.button("Limpar"):
        st.session_state.plano = []
        st.rerun()

# Abas
tab1, tab2, tab3 = st.tabs(["Captura", "Plano", "Análise"])

# TAB 1
with tab1:
    st.header("Captura de Ações")
    
    if not cliente:
        st.info("Digite o cliente na barra lateral")
    else:
        acao_nome = st.selectbox("Ação", [a.get("acao", "") for a in acoes_banco])
        acao = next((a for a in acoes_banco if a.get("acao") == acao_nome), None)
        
        if acao:
            col1, col2, col3 = st.columns(3)
            col1.metric("Categoria", acao.get("categoria", ""))
            col2.metric("Impacto", acao.get("impacto_padrao", 0))
            col3.metric("Esforço", acao.get("esforco_padrao", 0))
            
            st.write(f"**What:** {acao.get('what', '')}")
            st.write(f"**Why:** {acao.get('why', '')}")
            st.write(f"**Where:** {acao.get('where', '')}")
            st.write(f"**How:** {acao.get('how', '')}")
            st.write(f"**Indicadores:** {acao.get('indicadores', '')}")
            
            data_inicio = st.date_input("Início", key="d1")
            duracao = st.number_input("Duração (dias)", value=acao.get("duracao_dias", 7), min_value=1, max_value=180)
            impacto = st.number_input("Impacto", value=acao.get("impacto_padrao", 3), min_value=1, max_value=5)
            esforco = st.number_input("Esforço", value=acao.get("esforco_padrao", 3), min_value=1, max_value=5)
            responsavel = st.text_input("Responsável")
            status = st.selectbox("Status", ["Planejado", "Em andamento", "Concluído"])
            notas = st.text_area("Notas")
            
            if st.button("Adicionar"):
                if responsavel:
                    score = (impacto * config.get("peso_impacto", 10)) - (esforco * config.get("peso_esforco", 2))
                    data_fim = datetime.combine(data_inicio, datetime.min.time()) + timedelta(days=duracao)
                    
                    if score >= 30:
                        pri = "P0"
                    elif score >= 20:
                        pri = "P1"
                    elif score >= 10:
                        pri = "P2"
                    elif score >= 0:
                        pri = "P3"
                    else:
                        pri = "P4"
                    
                    st.session_state.plano.append({
                        "acao": acao_nome,
                        "categoria": acao.get("categoria", ""),
                        "responsavel": responsavel,
                        "data_inicio": data_inicio,
                        "data_fim": data_fim.date(),
                        "duracao": duracao,
                        "impacto": impacto,
                        "esforco": esforco,
                        "score": score,
                        "prioridade": pri,
                        "status": status,
                        "notas": notas,
                        "what": acao.get("what", ""),
                        "why": acao.get("why", ""),
                        "where": acao.get("where", ""),
                        "how": acao.get("how", ""),
                        "indicadores": acao.get("indicadores", "")
                    })
                    st.success("Ação adicionada!")
                    st.rerun()
                else:
                    st.error("Digite o responsável")

# TAB 2
with tab2:
    st.header("Plano 5W2H")
    
    if not st.session_state.plano:
        st.info("Nenhuma ação adicionada")
    else:
        total = len(st.session_state.plano)
        score_total = sum(a["score"] for a in st.session_state.plano)
        score_medio = score_total / total if total > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", total)
        col2.metric("Score Total", f"{score_total:.1f}")
        col3.metric("Score Médio", f"{score_medio:.1f}")
        col4.metric("Impacto", sum(a["impacto"] for a in st.session_state.plano))
        
        df = pd.DataFrame([{
            "ID": i+1,
            "Ação": a["acao"],
            "Categoria": a["categoria"],
            "Responsável": a["responsavel"],
            "Início": a["data_inicio"],
            "Fim": a["data_fim"],
            "Impacto": a["impacto"],
            "Esforço": a["esforco"],
            "Score": f"{a['score']:.1f}",
            "Prioridade": a["prioridade"]
        } for i, a in enumerate(st.session_state.plano)])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.write("---")
        
        for i, a in enumerate(st.session_state.plano):
            st.write(f"**{i+1}. {a['acao']}** ({a['prioridade']})")
            st.write(f"What: {a['what']}")
            st.write(f"Why: {a['why']}")
            st.write(f"Where: {a['where']}")
            st.write(f"How: {a['how']}")
            st.write(f"Responsável: {a['responsavel']} | Início: {a['data_inicio']} | Fim: {a['data_fim']}")
            st.write(f"Impacto: {a['impacto']} | Esforço: {a['esforco']} | Score: {a['score']:.1f}")
            if a['notas']:
                st.write(f"Notas: {a['notas']}")
            
            if st.button(f"Remover {i+1}", key=f"r{i}"):
                st.session_state.plano.pop(i)
                st.rerun()
            
            st.write("---")

# TAB 3
with tab3:
    st.header("Análise")
    
    if st.session_state.plano:
        cat = {}
        for a in st.session_state.plano:
            c = a["categoria"]
            cat[c] = cat.get(c, 0) + 1
        
        st.write("Categoria")
        st.bar_chart(pd.DataFrame(list(cat.items()), columns=["Categoria", "Qtd"]).set_index("Categoria"))
        
        scores = [a["score"] for a in st.session_state.plano]
        col1, col2, col3 = st.columns(3)
        col1.metric("Score Max", f"{max(scores):.1f}")
        col2.metric("Score Min", f"{min(scores):.1f}")
        col3.metric("Score Médio", f"{sum(scores)/len(scores):.1f}")
        
        st.write("Scores")
        st.bar_chart(pd.DataFrame([{"Ação": a["acao"][:15], "Score": a["score"]} for a in st.session_state.plano]).set_index("Ação"))
    else:
        st.info("Nenhuma ação")

st.write("---")
st.write("5W2H v1.0")
