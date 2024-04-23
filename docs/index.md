# Home

## Introdução

Este projeto é a criação de uma API pública de consulta com finalidade de analise de dados de vitivinicultura oriundos do site da embrapa - arquivos CSV. - [aqui](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).

Os dados são relativos:

- Produção.
- Processamento.
- Comercialização.
- Importação.
- Exportação.

A API será utilizada para alimentar uma base de dados de um modelo de Machine Learning.

## Objetivos

- Construção de  uma Rest API em Python que faça consulta dos dados no site da Embrapa.
- Documentar a API.
- Criação de método de autenticação  - JWT.
- Plano de deploy da API
- Apresentar um MVP com o deploy e link.

## Tecnologias Utilizadas e Dependências

- Python: 3.12.2
- FastAPI
- Uvicorn
- SQLAlchem
- Pandas
- Aiosqlite
- Greenlet
- Isort:
- Taskipy
- Blue
- Httpx

---

## Tutorial de uso

Pré-requisitos:

- Python
- Poetry

### Instalação do Pyenv e Poetry

Usando pyenv e pip ou pipx 

1 - Instale o `pyenv` seguindo as instruções em: [pyenv](https://github.com/pyenv/pyenv#installation)

```py
pip install pyenv 
```

ou

```py
pipx install pyenv
```

2 - Use o `pyenv` para instalar a versão correta do Python:

```py
pyenv install 3.12.2
```

3 - Instale o Poetry usando pip ou pipix:

```py
pip install poetry
```

### Instalação e Configuração do Ambiente

1 - Clone este repositório:

```py
git clone https://github.com/seu-usuario/nome-do-projeto.git
cd nome-do-projeto
```

2 - Já dentro da pasta, instale as dependências e crie o ambiente virtual usando o Poetry:

```py
poetry install
```

3 - Ative o ambiente virtual:

```py
poetry shell
```

### Executando o Projeto

Para executar o projeto, use o seguinte comando:

```py
task run
```

---

## Tarefas Disponíveis

Este projeto utiliza o Taskipy para gerenciar tarefas comuns. Aqui estão algumas tarefas disponíveis:

- ```task format```: Formata o código usando o Black e organiza as importações com o isort.
- ```task run```: Inicia o servidor de desenvolvimento.

Você pode executar qualquer tarefa usando o comando `poetry run task NOME_DA_TAREFA` adicinada no arquivo pyproject.toml:
```py title="Exemplo task"
[tool.taskipy.tasks]
format = 'blue .  && isort .'
run = 'uvicorn embrapa.app:app --reload'
```