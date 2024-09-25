import streamlit as st

def main():
    st.markdown('<h1 class="title">Home</h1>', unsafe_allow_html=True)
    st.markdown("""### Projeto: Importação de PDF de Notas de Corretagem

#### Objetivo
O objetivo deste projeto é desenvolver um sistema automatizado para a importação de arquivos PDF contendo notas de corretagem, facilitando a extração, processamento e análise das informações financeiras. 
O sistema permitirá que usuários importem suas notas de corretagem diretamente em um formato estruturado, proporcionando maior eficiência e precisão no controle de investimentos.
Dowload das cotações atual dos tickers e assim atualizando os valores do portifolio.


#### Tecnologias e Ferramentas
O sistema será desenvolvido com as seguintes tecnologias:
- **Python**: Linguagem principal para processamento e automação.
- **Bibliotecas de PDF**: Utilização da biblioteca camelot para a leitura e extração dos dados de PDF.
- **pandas**: Para manipulação e estruturação dos dados extraídos.
- **yfinance**: Para dowloados da cotação atualizado dos tickers.                
- **plotly**: para montagens dos gráficos.   
- **poetry**: para gerenciamentos das depedências 
- **Banco de Dados**:  PostgreSQL para armazenamento dos dados processados .
- **Interface Gráfica**: Desenvolvimento de uma interface gráfica usando o streamlit, para que usuários possam carregar os PDFs e visualizar os dados.

#### Fluxo de Importação
1. **Seleção da corretora**: O usuário carrega o arquivo PDF da nota de corretagem através da interface.
2. **Upload do PDF**: O usuário carrega o arquivo PDF da nota de corretagem através da interface.
3. **Extração de Dados**: O sistema lê o conteúdo do PDF, identificando os campos essenciais como:
   - Data da operação
   - Tipo de operação (compra/venda)
   - Ativo negociado (ações, opções, etc.)
   - Quantidade
   - Preço unitário
   - Valor total
   - Taxas e impostos
4. **Validação e Transformação**: Os dados extraídos são validados e transformados em um formato estruturado através de views
5. **Exportação**: O usuário pode exportar os dados para uma planilha CSV .

""")
    st.write('')
    st.write('')
    st.text('Link do projeto')
    st.link_button("Projeto", "https://github.com/robertoricci/app_notas_corretagem")
    st.write('')
    st.text('Link dos PDFs de Notas fiscais de corretagem')
    st.link_button("PDFs", "https://github.com/robertoricci/app_notas_corretagem/tree/main/NotasCorretagem")
    
if __name__ == "__main__":
   main()




