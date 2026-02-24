import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="5W2H", layout="wide", initial_sidebar_state="expanded")

# Load data
with open("data/acoes.json", encoding="utf-8") as f:
    data = json.load(f)

acoes = data["acoes"]
config = data["config"]

# Init session
if "plan" not in st.session_state:
    st.session_state.plan = []

# Title
st.title("Diagnostico 5W2H")

# Sidebar
with st.sidebar:
    st.header("Setup")
    client = st.text_input("Client Name")
    meeting_date = st.date_input("Meeting Date")
    if st.button("Clear Plan"):
        st.session_state.plan = []
        st.rerun()

# Main tabs
tab1, tab2, tab3 = st.tabs(["Add Action", "Plan", "Analysis"])

# TAB 1: Add Action
with tab1:
    st.header("Add Action")
    
    if not client:
        st.warning("Enter client name in sidebar")
    else:
        action_list = [a["acao"] for a in acoes]
        selected_action = st.selectbox("Select Action", action_list)
        
        action_data = next(a for a in acoes if a["acao"] == selected_action)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", action_data["categoria"])
        col2.metric("Impact", action_data["impacto_padrao"])
        col3.metric("Effort", action_data["esforco_padrao"])
        
        st.write("**What:** " + action_data["what"])
        st.write("**Why:** " + action_data["why"])
        st.write("**Where:** " + action_data["where"])
        st.write("**How:** " + action_data["how"])
        st.write("**Indicators:** " + action_data["indicadores"])
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", key="start")
            duration = st.number_input("Duration (days)", value=7, min_value=1, max_value=180)
            impact = st.number_input("Impact (1-5)", value=3, min_value=1, max_value=5)
        
        with col2:
            effort = st.number_input("Effort (1-5)", value=3, min_value=1, max_value=5)
            owner = st.text_input("Owner")
            status = st.selectbox("Status", ["Planned", "Running", "Done"])
        
        notes = st.text_area("Notes")
        
        if st.button("Add", use_container_width=True):
            if not owner:
                st.error("Enter owner name")
            else:
                score = (impact * config["peso_impacto"]) - (effort * config["peso_esforco"])
                end_date = datetime.combine(start_date, datetime.min.time()) + timedelta(days=duration)
                
                st.session_state.plan.append({
                    "action": selected_action,
                    "category": action_data["categoria"],
                    "owner": owner,
                    "start": start_date,
                    "end": end_date.date(),
                    "days": duration,
                    "impact": impact,
                    "effort": effort,
                    "score": score,
                    "status": status,
                    "notes": notes,
                    "what": action_data["what"],
                    "why": action_data["why"],
                    "where": action_data["where"],
                    "how": action_data["how"],
                    "indicators": action_data["indicadores"]
                })
                st.success("Added!")
                st.rerun()

# TAB 2: Plan
with tab2:
    st.header("5W2H Plan")
    
    if not st.session_state.plan:
        st.info("No actions added")
    else:
        n = len(st.session_state.plan)
        total_score = sum(a["score"] for a in st.session_state.plan)
        avg_score = total_score / n if n > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", n)
        col2.metric("Total Score", f"{total_score:.1f}")
        col3.metric("Avg Score", f"{avg_score:.1f}")
        col4.metric("Total Impact", sum(a["impact"] for a in st.session_state.plan))
        
        st.divider()
        
        df_data = []
        for i, a in enumerate(st.session_state.plan):
            df_data.append({
                "N": i+1,
                "Action": a["action"],
                "Category": a["category"],
                "Owner": a["owner"],
                "Start": str(a["start"]),
                "End": str(a["end"]),
                "Days": a["days"],
                "Impact": a["impact"],
                "Effort": a["effort"],
                "Score": f"{a['score']:.1f}",
                "Status": a["status"]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        for i, a in enumerate(st.session_state.plan):
            st.write(f"**{i+1}. {a['action']}** (Score: {a['score']:.1f})")
            st.write(f"Category: {a['category']} | Owner: {a['owner']} | Status: {a['status']}")
            st.write(f"Start: {a['start']} | End: {a['end']} | Days: {a['days']}")
            st.write(f"Impact: {a['impact']}/5 | Effort: {a['effort']}/5")
            st.write(f"What: {a['what']}")
            st.write(f"Why: {a['why']}")
            st.write(f"Where: {a['where']}")
            st.write(f"How: {a['how']}")
            if a['notes']:
                st.write(f"Notes: {a['notes']}")
            
            if st.button(f"Delete {i+1}", key=f"del{i}"):
                st.session_state.plan.pop(i)
                st.rerun()
            
            st.divider()

# TAB 3: Analysis
with tab3:
    st.header("Analysis")
    
    if not st.session_state.plan:
        st.info("No actions")
    else:
        cat_dict = {}
        for a in st.session_state.plan:
            c = a["category"]
            cat_dict[c] = cat_dict.get(c, 0) + 1
        
        st.write("By Category")
        df_cat = pd.DataFrame(list(cat_dict.items()), columns=["Category", "Count"])
        st.bar_chart(df_cat.set_index("Category"))
        
        st.divider()
        
        scores = [a["score"] for a in st.session_state.plan]
        col1, col2, col3 = st.columns(3)
        col1.metric("Max Score", f"{max(scores):.1f}")
        col2.metric("Min Score", f"{min(scores):.1f}")
        col3.metric("Avg Score", f"{sum(scores)/len(scores):.1f}")
        
        st.write("Scores")
        df_scores = pd.DataFrame([{"Action": a["action"][:20], "Score": a["score"]} for a in st.session_state.plan])
        st.bar_chart(df_scores.set_index("Action"))

st.divider()
st.write("5W2H v1.0")
