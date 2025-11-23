import streamlit as st
import database_manager as bc

bc.criar_tabela()

st.set_page_config(page_title="Focus Forge", page_icon="🛡️")

st.title("🛡️ FOCUS FORGE - Quartel General")

st.divider()


historico = bc.ler_historico()


if not historico:
    st.warning("Nenhuma missão realizada ainda, soldado. Vá estudar!")
else:
  
    st.dataframe(historico, use_container_width=True)

    st.divider()
    
    st.metric("Missões Cumpridas", len(historico))