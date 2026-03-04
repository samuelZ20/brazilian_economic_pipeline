import streamlit as st
import pandas as pd
from deltalake import DeltaTable
import plotly.express as px
import os
from dotenv import load_dotenv

# 1. Configurações Iniciais
load_dotenv()
st.set_page_config(page_title="Lakehouse Econômico - UFLA", layout="wide", page_icon="🏦")

# Estilização básica
st.title("🏦 Dashboard de Indicadores Econômicos")
st.markdown("Visualização da **Camada Gold** processada via Airflow & Delta Lake")

# 2. Configuração de Conexão (MinIO via Docker Network)
storage_options = {
    "endpoint_url": os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    "aws_access_key_id": os.getenv("MINIO_ACCESS_KEY", "admin"),
    "aws_secret_access_key": os.getenv("MINIO_SECRET_KEY", "password"),
    "region": "us-east-1",
    "allow_http": "true"
}

@st.cache_data(ttl=600)
def load_data():
    """Lê a tabela Delta da camada Gold no MinIO"""
    try:
        uri = "s3://bacen-lake/gold/economic_indicators_comparison/"
        dt = DeltaTable(uri, storage_options=storage_options)
        df = dt.to_pandas()
        df['data'] = pd.to_datetime(df['data'])
        
        # Converte o formato do DataFrame de wide para long, caso não exista a coluna 'indicador'
        if 'indicador' not in df.columns:
            value_cols = [c for c in df.columns if c != 'data']
            df = df.melt(id_vars=['data'], value_vars=value_cols, var_name='indicador', value_name='valor')
            
        return df.sort_values('data')
    except Exception as e:
        st.error(f"Erro ao carregar dados da Camada Gold: {e}")
        return pd.DataFrame()

# 3. Carregamento e Filtros
df_gold = load_data()

if not df_gold.empty:
    # Barra lateral para filtros
    st.sidebar.header("⚙️ Configurações")
    available_indicators = df_gold['indicador'].unique().tolist()
    selected_indicators = st.sidebar.multiselect(
        "Selecione os indicadores:",
        options=available_indicators,
        default=available_indicators
    )

    df_filtered = df_gold[df_gold['indicador'].isin(selected_indicators)]

    # 4. Métricas de Destaque (Cards)
    col1, col2, col3 = st.columns(3)
    
    # Exemplo: Último valor da SELIC e IPCA
    for idx, (col, label) in enumerate(zip([col1, col2, col3], selected_indicators[:3])):
        latest = df_gold[df_gold['indicador'] == label].iloc[-1]
        col.metric(label, f"{latest['valor']:.2f}%", help=f"Última atualização: {latest['data'].date()}")

    # 5. Visualização Gráfica
    st.subheader("📈 Evolução das Taxas")
    fig = px.line(
        df_filtered, 
        x="data", 
        y="valor", 
        color="indicador",
        markers=True,
        template="plotly_dark",
        labels={"valor": "Taxa Anual (%)", "data": "Mês/Ano"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # 6. Tabela de Dados (Visão Técnica)
    with st.expander("📄 Visualizar Tabela de Dados (Delta Table)"):
        st.dataframe(df_filtered.sort_values(by="data", ascending=False), use_container_width=True)

else:
    st.warning("⚠️ Nenhum dado encontrado na Camada Gold. Verifique se a DAG `3_camada_gold` rodou com sucesso!")

st.divider()
st.caption("Projeto desenvolvido por Samuel Frizzone Cardoso - Ciência da Computação (UFLA)")