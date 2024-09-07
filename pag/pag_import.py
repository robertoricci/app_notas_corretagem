import streamlit as st
import os
import camelot
import pandas as pd
import logging
import util.util as util
import tempfile
from unidecode import unidecode
from configs.rules.notas import rules_dict
logging.basicConfig(level=logging.INFO)
from configs.bd.postgree import RDSPostgreSQLManager
import time

def read_pdf(file):
    pass


class PDFTableExtractor:
    def __init__(self, file_name,name,configs):

        self.path = os.path.abspath(f"files/pdf{configs['name'].lower()}/")
        print('SELVPATHY' +  self.path )
        self.csv_path = "files/csv/"
        self.file_name = file_name
        self.name = name
        self.configs = configs

    def start(self):
        
        logging.info(f"Start pdf - {self.file_name}")
        
        header = self.get_table_data(self.configs["header_table_areas"], self.configs["header_columns"],self.configs["header_fix"])
        
        main = self.get_table_data(self.configs["table_areas"], self.configs["columns"],self.configs["fix"])

        small = self.get_table_data(self.configs["small_table_areas"], self.configs["small_columns"],self.configs["small_fix"])

        main = self.add_infos(header,main)
        
        small = self.add_infos(header, small)

        main = self.sanitize_column_names(main)
        if self.configs["small_sanitize"]:
            small = self.sanitize_column_names(small)

        logging.info(f"Saving csv - {self.file_name}")
        self.save_csv(main, self.name)
        self.save_csv(small, f"{self.name}_small")

        logging.info(f"Sending to DB - {self.file_name}")
        self.send_to_db(main, f"Fatura_{self.configs['name']}".lower())
        self.send_to_db(small, f"Fatura_{self.configs['name']}_small".lower())

        sql = RDSPostgreSQLManager()
      
        return {"main": main, "small": small}
    def get_table_data(self, table_areas, table_columns, fix = True):
        tables = camelot.read_pdf(
            self.file_name,
            flavor=self.configs["flavor"],
            table_areas=table_areas,
            columns=table_columns,
            strip_text=self.configs["strip_text"],
            pages=self.configs["pages"],
            password=self.configs["password"],
        )

        table_content = [self.fix_header(page.df) if fix else page.df for page in tables]

        result = pd.concat(table_content, ignore_index=True) if len(table_content) > 1 else table_content[0]
        return result

    def save_csv(self, df, file_name):

        if not os.path.exists(self.csv_path):
            print(self.csv_path)
            os.makedirs(self.local_path, exist_ok=True)
        ##path = os.path.join(self.csv_path, f"{file_name}.csv")
        path =  f"{self.csv_path}/{file_name}.csv"
        df.to_csv(path, sep=";", index=False)

    def add_infos(self, header, content):
        infos = header.iloc[0]
        df = pd.DataFrame([infos.values] * len(content), columns=header.columns)
        content = pd.concat([content.reset_index(drop=True),df.reset_index(drop=True)], axis=1)
        content["Data de Inserção"] = pd.Timestamp('today').normalize()

        return content

    @staticmethod
    def fix_header(df):
        df.columns = df.iloc[0]
        df = df.drop(0)
        df = df.drop(df.columns[0], axis=1)
        return df

    def sanitize_column_names(self, df):
        df.columns = df.columns.map(lambda x: unidecode(x))
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace(r'\W', '', regex=True)
        df.columns = df.columns.str.lower()
        return df

    @staticmethod
    def send_to_db(df, table_name):
        try:
            connection = RDSPostgreSQLManager().alchemy()
            print(connection)
            df.to_sql(table_name, connection, if_exists="append", index=False)
            logging.info(f"Success to save into {table_name}")
        except Exception as e:
            print('erro ao inserir')
            logging.error(e)

def list_files(folder):
    try:
        files = [os.path.splitext(f)[0] for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files
    except FileNotFoundError:
        logging.info(f"A pasta '{folder}' não foi encontrada.")
        return []
    except Exception as e:
        logging.info(f"Ocorreu um erro: {e}")
        return []

def click_button():
    st.session_state.button = not st.session_state.button

def disable(b):
    st.session_state["disabled"] = True
    print(b)

def check_filename_contains(filenames,corretora):
    return [filename for filename in filenames if corretora not in filename.lower()]
def main():

    tables = util.dic_tables()
    st.write(tables)

    st.title("Upload de Múltiplos PDFs")


    if "disabled" not in st.session_state:
          st.session_state["disabled"] = False

    if "button_disabled" not in st.session_state:
        st.session_state.button_disabled = False


    if "processando" not in st.session_state:
        st.session_state.processando = False
    
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center; padding: 0rem 0rem 0rem'>Corretora</h2>", unsafe_allow_html=True)
        corretora = st.selectbox('Escolha a corretora',tables)
        uploaded_files = st.file_uploader("Escolha os arquivos PDF", type="pdf", accept_multiple_files=True)
        if uploaded_files:
                    col1,col2 = st.columns([6,6])
                    if st.button("Processar arquivos"):
                      if st.session_state.processando:
                        return
                      else:
                        st.session_state.processando = True
                        filenames = [uploaded_file.name for uploaded_file in uploaded_files]
                        not_matching_filenames = check_filename_contains(filenames,corretora)
                        if (not_matching_filenames):
                            st.error(f'Estes arquivos são diferente da selecionada {corretora}')
                            st.table(not_matching_filenames)
                            st.session_state.processando = False
                            return
                        if (corretora != 'Selecionar'):
                            with col1:
                                with st.spinner("processando arquivos..."):
                                    st.session_state.button_disabled = True
                                    st.toast('Processando')
                                    for uploaded_file in uploaded_files:
                                            newfilename = uploaded_file.name.rsplit('.', maxsplit=1)[0]
                                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                                                temp.write(uploaded_file.getbuffer())
                                            extractor = PDFTableExtractor(temp.name,newfilename, configs=rules_dict[corretora]).start()

                                            os.remove(temp.name)  # clean up
                                            st.write('Arquivos processados')
                                            st.session_state.button_disabled = False
                                            st.session_state.processando = False 
                                            st.rerun()
                        else:
                            st.session_state.processando = False
                            st.error('Selecionar a corretora')


if __name__ == "__main__":
   main()




