import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
df = pd.read_excel("cancelamentos.xls", sheet_name="CANCELAMENTOS")

df["Data"] = pd.to_datetime(df["Data"])
df = df.sort_values("Data")
df["Mês"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

month = st.sidebar.selectbox("Mês:", df["Mês"].unique())

operador = st.sidebar.multiselect(
    "Operadores:",
    df["Operador"].unique(),
    placeholder="Selecione um operador ou mais..."
)

tipo_canc_op = st.sidebar.multiselect(
    "Tipos de Cancelamentos:",
    ["PASSOU 2X", "NAO COLOCOU CPF", "CLIENTE DESISTIU", "TESTE", "CODIGO ERRADO", "ERRO EXTERNO"],
    default=["PASSOU 2X", "NAO COLOCOU CPF", "CODIGO ERRADO"]
)

estorno = st.sidebar.selectbox(
    "Tipo de Estorno:", 
    df["Tipo de Estorno"].unique(), 
    index= None, 
    placeholder="Selecione o tipo de estorno..."
)

status = st.sidebar.selectbox(
    "Status:", 
    df["Status"].unique(), 
    index= None, 
    placeholder="Selecione o status..."
)


df_filtered = df[df["Mês"] == month]
if operador: 
    df_filtered = df_filtered[df_filtered["Operador"].isin(operador)]
if tipo_canc_op:
    df_filtered = df_filtered[df_filtered["Tipo de Cancelamento"].isin(tipo_canc_op)]
if estorno:
    df_filtered = df_filtered[df_filtered["Tipo de Estorno"] == estorno]
if status:
    df_filtered = df_filtered[df_filtered["Status"] == status]
st.dataframe(df_filtered)

col1, col2 = st.columns(2)
fig = px.pie(df_filtered, values="Valor", names="Operador", title="Estorno por operador")
col1.plotly_chart(fig)