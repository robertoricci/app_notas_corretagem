import streamlit as st
from configs.bd.postgree import RDSPostgreSQLManager
import pandas as pd
import altair as alt
import yfinance as yf

@st.cache_data(show_spinner="Buscando Cotações...", ttl=60*5)
def buscar_cotacao(l_ticker,b3 ):
    # Usando list comprehension para adicionar '.SA' no final de cada ação
    if (b3):
        l_ticker = [acao + '.SA' for acao in l_ticker]

    df_tickers = yf.download(l_ticker, period="1d")['Close']

    return df_tickers


def montar_dataframe_ticker(df ):
   
   l_ticker = list(df.index)
   b3 = True
   df_tickers = buscar_cotacao(l_ticker,b3 )
   df_tickers = df_tickers.reset_index(drop=True)
   df_tickers = df_tickers.melt(var_name='Ticker',value_name='cotacao_atual')

   df_tickers['ticker'] = df_tickers['Ticker'].str.replace('.SA', '', regex=False)

   df_tickers.drop(columns=['Ticker'], inplace=True)

   df = pd.merge(df,df_tickers, left_on='ticker',right_on='ticker', how='left')

   df['valor_atual'] = df['qted']  * df['cotacao_atual']

   df.insert(0, 'image', '')
   df['image'] = 'https://raw.githubusercontent.com/robertoricci/icon-b3/main/icon/'+df['ticker']+'.png'

   return df
   
def selecionar_dados():
    query = 'select * from public.notas_corretagem'
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return df 

def main():
    
    st.markdown('<h1 class="title">Dasboard</h1>', unsafe_allow_html=True)

    df = selecionar_dados()
   


    # if (df.size  > 0):

    #     df['data_de_pregao'] = pd.to_datetime(df['data_de_pregao']).dt.date

    #     dt_min = df["data_de_pregao"].min()
    #     dt_max = df["data_de_pregao"].max()


    #     data_selecionada = st.date_input("Selecione o intervalo de datas:",value=[dt_min, dt_max],min_value=dt_min,max_value=dt_max)
        
    #     try:
    #         data_ini_sel =  data_selecionada[0]
    #     except:
    #         data_ini_sel =  dt_min

    #     try:
    #         data_fim_sel =  data_selecionada[1]
    #     except:
    #         data_fim_sel =  dt_max

    #     df_filtered = df[df["data_de_pregao"].between(data_ini_sel, data_fim_sel)]
        
        
    #     corretora_selecionada = st.multiselect("Selecione a Corretora:",options=df_filtered["corretora"].unique(),  default=df_filtered["corretora"].unique())
    #     ticker_selecionado = st.multiselect("Selecione o Ticker:",options=df_filtered["ticker"].unique(),  default=df_filtered["ticker"].unique())

    #     df_filtered = df_filtered[(df_filtered["corretora"].isin(corretora_selecionada)) & 
    #                 (df_filtered["ticker"].isin(ticker_selecionado)) 
    #                 ]
        
    #     df_mov = df_filtered.groupby('cv')['movimentacao'].sum().reset_index()

    #     col1,col2,col3,col4 = st.columns([3,3,3,3])
    
    #     with col1:
    #         st.html('<span class="Medio_indicator"></span>')
    #         st.metric(label='Total Tickers', value=len(df_filtered['ticker'].unique()))

    #     with col2:
    #         st.html('<span class="Medio_indicator"></span>')
    #         compra = df_mov[df_mov['cv']=='Compra'].values[0][1]
    #         st.metric(label='Compra', value=f"R$ {compra:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    #     with col3:
    #         st.html('<span class="Medio_indicator"></span>')
    #         venda = df_mov[df_mov['cv']=='Venda'].values[0][1]
    #         st.metric(label='Venda', value=f"R$ {venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    #     with col4:
    #         st.html('<span class="Medio_indicator"></span>')
    #         saldo =  venda - abs(compra)
    #         st.metric(label='Saldo', value=f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    #     df_soma = df_filtered.groupby('ticker')['qted'].sum()

    #     df_soma = df_soma.to_frame()

    #     df_tickers = montar_dataframe_ticker(df_soma)
        
    #     st.markdown('<h3 class="subtitulo">Portifólio</h3>', unsafe_allow_html=True)

    #     st.dataframe(df_tickers,hide_index= False, column_config={"image": st.column_config.ImageColumn(help='IMag'), 
    #                                             }
    #                             ,use_container_width=False)

    #     st.write('')
    #     st.write('')
    
    #     st.markdown('<h3 class="subtitulo">Extrato</h3>', unsafe_allow_html=True)
    #     st.dataframe(df_filtered,use_container_width=True)

    
    #     st.markdown('<h3 class="subtitulo">Quantidade por ticker</h3>', unsafe_allow_html=True)
    #     qted_chart = alt.Chart(df_filtered).mark_bar().encode(
    #     x='ticker:N',
    #     y='qted:Q',
    #     color='ticker:N'
    #     ).properties(
    #     title=''
    #     )
    #     st.altair_chart(qted_chart, use_container_width=True)


    #     # st.header("Movimentação ao longo do tempo")
    #     # movimentacao_chart = alt.Chart(df_filtered).mark_line().encode(
    #     #     x='data_de_pregao:T',
    #     #     y='movimentacao:Q',
    #     #     color='ticker:N'
    #     # ).properties(
    #     #     title='Movimentação por Mercadoria ao Longo do Tempo'
    #     # )
    #     # st.altair_chart(movimentacao_chart, use_container_width=True)  

    #     df_agrupado = df_filtered.groupby(['data_de_pregao'])['movimentacao'].sum().reset_index()

    #     ##df_agrupado.set_index('data_de_pregao',inplace=True)


    #     ##df_filtered.set_index('data_de_pregao',inplace=True)

    #     ##st.dataframe(df_agrupado)

    #     import plotly.express as px


    #     # fig = px.line(df_agrupado, 
    #     #             x='data_de_pregao', 
    #     #             y='movimentacao', 
    #     #             color='ticker', 
    #     #             title='Movimentação por Data e Ticker')

    #     # # Exibir o gráfico no Streamlit
    #     # st.plotly_chart(fig)

    
    #     df_agrupado['data_de_pregao'] = pd.to_datetime(df_agrupado['data_de_pregao'])
    
    #     fig = px.line(df_agrupado, x='data_de_pregao', y='movimentacao', title='')
        
    #     st.markdown('<h3 class="subtitulo">Movimentação ao Longo do Tempo</h3>', unsafe_allow_html=True)
    #     st.plotly_chart(fig)

    #     df_sum = df_filtered.groupby('ticker')['movimentacao'].sum().reset_index()

    #     # Criar o gráfico de barras
    #     fig = px.bar(df_sum, 
    #                 x='ticker', 
    #                 y='movimentacao', 
    #                 color='ticker', 
    #                 title='')

    
    #     st.markdown('<h3 class="subtitulo">Movimentação port Ticker</h3>', unsafe_allow_html=True)
    #     st.plotly_chart(fig)                      



if __name__ == "__main__":
   main()




