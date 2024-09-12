import streamlit as st


def main():
    st.write('home')

    st.markdown("""### Projeto: Importação de PDF de Notas de Corretagem

#### Objetivo
O objetivo deste projeto é desenvolver um sistema automatizado para a importação de arquivos PDF contendo notas de corretagem, facilitando a extração, processamento e análise das informações financeiras. O sistema permitirá que usuários importem suas notas de corretagem diretamente em um formato estruturado, proporcionando maior eficiência e precisão no controle de investimentos.

#### Descrição do Problema
Atualmente, o processo de gerenciamento de investimentos através de notas de corretagem é manual e sujeito a erros. Investidores recebem documentos em formato PDF de suas corretoras, com informações detalhadas sobre transações de compra e venda de ativos financeiros. No entanto, a extração manual desses dados para planilhas ou sistemas internos é demorada e propensa a falhas.

#### Solução Proposta
Este projeto visa desenvolver uma solução para:
1. **Carregar PDFs de notas de corretagem**: Importar arquivos PDF fornecidos pelas corretoras.
2. **Extrair dados relevantes**: Utilizar técnicas de processamento de texto para identificar e extrair informações-chave, como data, ativos negociados, quantidade, preços, taxas e impostos.
3. **Transformar em dados estruturados**: Converter os dados extraídos em um formato adequado para análise, como tabelas ou arquivos CSV.
4. **Integração com outros sistemas**: Possibilitar a exportação dos dados para sistemas de controle financeiro ou plataformas de análise de portfólio.

#### Tecnologias e Ferramentas
O sistema será desenvolvido com as seguintes tecnologias:
- **Python**: Linguagem principal para processamento e automação.
- **Bibliotecas de PDF**: Utilização de bibliotecas como `PyPDF2`, `pdfplumber` ou `tabula-py` para a leitura e extração dos dados de PDF.
- **Pandas**: Para manipulação e estruturação dos dados extraídos.
- **Banco de Dados**: MySQL ou PostgreSQL para armazenamento dos dados processados (se necessário).
- **Interface Gráfica ou API**: Desenvolvimento de uma interface gráfica ou API para que usuários possam carregar os PDFs e visualizar os dados.

#### Fluxo de Trabalho
1. **Upload do PDF**: O usuário carrega o arquivo PDF da nota de corretagem através da interface.
2. **Extração de Dados**: O sistema lê o conteúdo do PDF, identificando os campos essenciais como:
   - Data da operação
   - Tipo de operação (compra/venda)
   - Ativo negociado (ações, opções, etc.)
   - Quantidade
   - Preço unitário
   - Valor total
   - Taxas e impostos
3. **Validação e Transformação**: Os dados extraídos são validados e transformados em um formato estruturado.
4. **Exportação e Integração**: O usuário pode exportar os dados para uma planilha CSV ou integrar com sistemas externos.

#### Desafios
- **Variedade de Formatos de PDF**: Notas de corretagem podem variar em layout de acordo com a corretora. Será necessário desenvolver uma lógica robusta para lidar com essas variações.
- **Precisão na Extração**: Garantir que todos os dados sejam extraídos corretamente, mesmo com variações no formato do PDF.
- **Segurança**: Proteger os dados sensíveis dos usuários durante o processo de importação e armazenamento.

#### Cronograma de Desenvolvimento
1. **Análise de requisitos**: 1 semana
2. **Desenvolvimento do módulo de leitura de PDF**: 2 semanas
3. **Desenvolvimento da extração e estruturação dos dados**: 3 semanas
4. **Integração com banco de dados e exportação**: 2 semanas
5. **Testes e validação**: 2 semanas
6. **Entrega final e documentação**: 1 semana

#### Conclusão
O projeto de importação de PDF de notas de corretagem proporcionará aos investidores uma solução prática e automatizada para o controle e análise de suas transações financeiras, otimizando tempo e reduzindo erros manuais. Com essa ferramenta, será possível integrar as informações de diversas corretoras em um único lugar, gerando relatórios e insights de maneira eficiente.
""")



if __name__ == "__main__":
   main()




