import streamlit as st
from configs.bd.postgree import RDSPostgreSQLManager

def selecionar_dados():
    query = "select distinct corretora||'-'||n_nota as notas from public.notas_corretagem"
    bd = RDSPostgreSQLManager()
    df = bd.execute_query(query)
    return df 


def excluir_nota(corretora,nota):
    
      bd = RDSPostgreSQLManager()
      ret = bd.execute_notas(corretora,nota)

      st.write(ret)

def main():
    st.write('Manutenção')

    df_notas = selecionar_dados()
    st.write(df_notas)

    corretora_nota = st.selectbox("Selecione a Corretora:",options=df_notas)

    if st.button('Excluir Nota de corretagem'):
        empresa, nota = corretora_nota.split("-")
        ret = excluir_nota(empresa,nota)
        st.write('excluindo NF' + str(ret))



if __name__ == "__main__":
   main()




