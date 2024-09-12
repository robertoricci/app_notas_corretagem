import streamlit as st
from configs.bd.postgree import RDSPostgreSQLManager
import pandas as pd
import altair as alt

def selecionar_dados():
    query = 'select * from public.notas_corretagem'
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return df 

def main():
    st.markdown("""
                <style>
                .title {
                text-align: center;
                }
                </style>
                """,unsafe_allow_html=True)
    st.markdown('<h1 class="title">Dasboard</h1>', unsafe_allow_html=True)

    df = selecionar_dados()

    df['data_de_pregao'] = pd.to_datetime(df['data_de_pregao']).dt.date

    dt_min = df["data_de_pregao"].min()
    dt_max = df["data_de_pregao"].max()


    data_selecionada = st.date_input("Selecione o intervalo de datas:",value=[dt_min, dt_max],min_value=dt_min,max_value=dt_max)
    
    try:
      data_ini_sel =  data_selecionada[0]
    except:
       data_ini_sel =  dt_min

    try:
      data_fim_sel =  data_selecionada[1]
    except:
       data_fim_sel =  dt_max

    df_filtered = df[df["data_de_pregao"].between(data_ini_sel, data_fim_sel)]
     
    
    corretora_selecionada = st.multiselect("Selecione a Corretora:",options=df_filtered["corretora"].unique(),  default=df_filtered["corretora"].unique())
    ticker_selecionado = st.multiselect("Selecione o Ticker:",options=df_filtered["ticker"].unique(),  default=df_filtered["ticker"].unique())

    df_filtered = df_filtered[(df_filtered["corretora"].isin(corretora_selecionada)) & 
                (df_filtered["ticker"].isin(ticker_selecionado)) 
                ]
    
    df_mov = df_filtered.groupby('cv')['movimentacao'].sum().reset_index()

    col1,col2,col3,col4 = st.columns([3,3,3,3])

    with col1:
        st.html('<span class="Medio_indicator"></span>')
        st.metric(label='Total Tickers', value=len(df_filtered['ticker'].unique()))

    with col2:
        st.html('<span class="Medio_indicator"></span>')
        compra = df_mov[df_mov['cv']=='Compra'].values[0][1]
        st.metric(label='Compra', value=f"R$ {compra:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    with col3:
        st.html('<span class="Medio_indicator"></span>')
        venda = df_mov[df_mov['cv']=='Venda'].values[0][1]
        st.metric(label='Venda', value=f"R$ {venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    with col4:
        st.html('<span class="Medio_indicator"></span>')
        saldo =  venda - abs(compra)
        st.metric(label='Saldo', value=f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    df_soma = df_filtered.groupby('ticker')['qted'].sum()

    st.write(df_soma)

    st.dataframe(df_filtered)


    st.header("Quantidade por ticker")
    qted_chart = alt.Chart(df_filtered).mark_bar().encode(
    x='ticker:N',
    y='qted:Q',
    color='ticker:N'
    ).properties(
    title='Quantidade Total por Ticker'
    )
    st.altair_chart(qted_chart, use_container_width=True)


    st.header("Movimentação ao longo do tempo")
    movimentacao_chart = alt.Chart(df_filtered).mark_line().encode(
        x='data_de_pregao:T',
        y='movimentacao:Q',
        color='ticker:N'
    ).properties(
        title='Movimentação por Mercadoria ao Longo do Tempo'
    )
    st.altair_chart(movimentacao_chart, use_container_width=True)  

    df_agrupado = df.groupby(['cv','data_de_pregao'])['movimentacao'].sum().reset_index()

    df_agrupado.set_index('data_de_pregao',inplace=True)
    

    # df_agrupado.set_index('data_de_pregao',inplace=True)                         



if __name__ == "__main__":
   main()




