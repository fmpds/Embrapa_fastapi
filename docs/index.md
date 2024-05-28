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
- Plano de deploy da API.
- Apresentar um MVP.

## Tecnologias Utilizadas e Dependências

- Python: 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- Pandas
- Aiosqlite
- Greenlet
- Unidecode
- Mkdocs
- Mkdocs-material
- Mkdocstring
- Taskipy
- Isort
- Blue
- Httpx
- Alembic
- Postgres
- Bcrypt
- Pydantic

---

## Tutorial de uso

### Instalação e Configuração do Ambiente

1 - Clone este repositório:

```py
git clone https://github.com/MLET-007/Embrapa_fastapi.git
cd Embrapa_fastapi
```

---

## Inicializando o projeto

Para rodar o projeto com docker basta executar.
```
docker-compose up -d 
``` 
Um container com a aplicação e postgres será criado para uso.

**Após rodar o comando espere 30 segundos antes de testar a aplicação**

---

## Criando um usuario e senha

Com o projeto rodando crie um usuario e senha para realizar a autenticação.

**Endpoint de criação de usuario: `http://localhost:8009/user`**

```json
{
  "username": "joao",
  "email": "joao@email.com.br",
  "full_name": "joao",
  "password": "123",
  "disabled": false
}
```

Após isso coloque os dados do usuario criados na pop-up do botão 'Authorize'.

## Realizando a carga de dados

Após todos esses passos execute o endpoint de importação e teste os outros endpoints.

**Endpoint de importação: `http://localhost:8009/docs#/default/importa_csv_api_importar_csv_site_embrapa_get`**