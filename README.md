# app_notas_corretagem
Importador de notas de corretagem 


#### Objetivo
O objetivo deste projeto é desenvolver um sistema automatizado para a importação de arquivos PDF contendo notas de corretagem, facilitando a extração, processamento e análise das informações financeiras. 
O sistema permitirá que usuários importem suas notas de corretagem diretamente em um formato estruturado, proporcionando maior eficiência e precisão no controle de investimentos.
Dowload das cotações atual dos tickers e assim atualizando os valores do portifolio.


#### Este projeto foi desenvolvido utilizando as seguintes tecnologias:


- **Python**: Linguagem principal para processamento e automação.
- **Bibliotecas de PDF**: Utilização da biblioteca camelot para a leitura e extração dos dados de PDF.
- **pandas**: Para manipulação e estruturação dos dados extraídos.
- **yfinance**: Para dowloados da cotação atualizado dos tickers.                
- **plotly**: para montagens dos gráficos.   
- **poetry**: para gerenciamentos das depedências 
- **Banco de Dados**:  PostgreSQL para armazenamento dos dados processados .
- **Interface Gráfica**: Desenvolvimento de uma interface gráfica usando o streamlit, para que usuários possam carregar os PDFs e visualizar os dados.


O projeto foi desenvolvido utilizando **Python 3.12** e as seguintes bibliotecas:

```toml
[tool.poetry.dependencies]
python = "^3.12"
streamlit = "^1.37.1"
streamlit-option-menu = "^0.3.13"
unidecode = "^1.3.8"
camelot-py = "^0.11.0"
psycopg2 = "^2.9.9"
sqlalchemy = "^2.0.32"
python-dotenv = "^1.0.1"
plotly = "^5.23.0"
yfinance = "^0.2.43"
opencv-python = "^4.10.0.84"
```

## Variáveis de Ambiente

O projeto requer as seguintes variáveis de ambiente para configurar o acesso ao banco de dados PostgreSQL:

- `DB_NAME`: Nome do banco de dados
- `DB_USER`: Nome de usuário do banco de dados
- `DB_PASSWORD`: Senha do banco de dados
- `DB_HOST`: Host do banco de dados (ex.: `localhost` ou IP do servidor)


## Configuração do Ambiente

para selecionar a versão do python com pyenv
```bash
   pyenv local 3.12.1
   ```

1. Clone o repositório:
   ```bash
   git clone https://github.com/robertoricci/app_notas_corretagem.git
   cd app_notas_corretagem
   ```

2. Instale as dependências usando Poetry:
   ```bash
   poetry install
   ```

3. Defina as variáveis de ambiente. Você pode criar um arquivo `.env` na raiz do projeto com o seguinte conteúdo, podendo utilizar o exemplo do arquivo '`.env_exemplo`:
   ```env
   DB_NAME=seu_nome_de_banco_de_dados
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=seu_host
   ```

4. Execute o projeto:
   ```bash
   streamlit run app.py
   ```


## Arquivos auxiliares

PDFs de notas de corretagem
```bash
   /NotasCorretagem
   ```

Scripts para criação das views 
```bash
   /Scripts_SQL
   ```

## Estrutura do Projeto

```plaintext
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── components/
│       ├── __init__.py
│       └── component1.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .env
├── pyproject.toml
└── README.md




