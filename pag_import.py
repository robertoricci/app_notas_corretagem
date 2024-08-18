import streamlit as st

import util.util as util

def main():

    tables = util.dic_tables()
    st.write(tables)
    
    st.title("Upload de Múltiplos PDFs")
    with st.container(border=True):
        col1,col2 = st.columns([6,6])
        st.markdown("<h2 style='text-align: center; padding: 0rem 0rem 0rem'>Corretora</h2>", unsafe_allow_html=True)
        tabela = st.selectbox('Escolha a corretora',tables)
        uploaded_files = st.file_uploader("Escolha os arquivos PDF", type="pdf", accept_multiple_files=True)
        if uploaded_files:
                if st.button("Enviar pdf"):
                    st.write(tabela)
                    if tabela != 'Selecionar':
                        st.write('PDf enviado')
                    else:
                        st.error('Selecionar a corretora')


if __name__ == "__main__":
   main()




