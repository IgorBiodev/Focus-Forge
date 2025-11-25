import streamlit as st
import database_manager as bc
import pandas as pd

st.set_page_config(page_title="Focus Forge", page_icon="🛡️", layout="wide")

st.title("🛡️ FOCUS FORGE - Quartel General")
st.markdown("---")


conexao = bc.sq.connect('forge.db')

query = "SELECT * FROM sessoes"


df = pd.read_sql_query(query, conexao)

if df.empty:
    st.warning("⚠️ Nenhuma missão realizada ainda. O banco de dados está vazio!")
else:
  
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Missões", len(df))
    with col2:
        # Tente pegar o 'tema' que mais aparece (moda). 
        # No pandas, a função é .mode()[0]
        tema_foco = df['tema'].mode()[0]
        st.metric("Foco Principal", tema_foco)

    st.markdown("---")

    col_grafico, col_tabela = st.columns([2, 1])

    with col_grafico:
        st.subheader("📊 Distribuição de Foco")
        
       
        contagem_temas = df['tema'].value_counts()
        
       
        st.bar_chart(contagem_temas)

    with col_tabela:
        st.subheader("📝 Histórico Bruto")
        
        st.dataframe(df, use_container_width=True, hide_index=True)