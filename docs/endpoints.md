# Endpoints

Para testar os endpoints citados abaixo, clique em Swagger ou Redoc para ser redirecionado para a documentação automatica feita pelo FastAPI

## Listagem de Endpoints

- Importar tabelas: Site Embrapa
- Importar tableas: Local
- Consulta tabela Comércio 
- Consulta tabela Exportação 
- Consulta tabela Importação 
- Consulta tabela Processamento 
- Consulta tabela Produção
- Criar usuário

---

### Importar tabelas: Site Embrapa

`GET` - **/api/importar_csv_site_embrapa?online=True**

Exemplo de resposta:

```json
    "Arquivos CSVs importados com sucesso do site da Embrapa!"
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os arquivos foram importados com sucesso.|
|500     | Servidor fora do ar |

---

### Importar tabelas: Local

`GET` - **/api/importar_csv_site_embrapa?online=False**

Exemplo de resposta:

```json
    "Arquivos CSVs importados com sucesso!"
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os arquivos foram importados com sucesso.|
|500     | Sem arquivos para ler|

---

### Comércio

`GET` - **/api/comercializacao/**

Exemplo de resposta:

```json
    [
        {
            "produto": "  Tinto",
            "ano": 1970,
            "litros": 83300735,
            "tipo": "VINHO DE MESA",
            "id": 2
        },
        {
            "produto": "  Rosado",
            "ano": 1970,
            "litros": 107681,
            "tipo": "VINHO DE MESA",
            "id": 3
        },
            ...
    ]
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os dados foram retornados com sucesso.|
|500     | Servidor fora do ar ou falta de importação dos arquivos|

---

### Exportação

`GET` - **/api/exportacao/**

Exemplo de resposta:

```json
    [
        {
            "pais": "Afeganistao",
            "ano": 1970,
            "quantidade": 0,
            "valor": 0.0,
            "id": 1
        },
        {
            "pais": "Africa do Sul",
            "ano": 1970,
            "quantidade": 0,
            "valor": 0.0,
            "id": 2
        },
            ...
    ]
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os dados foram retornados com sucesso.|
|500     | Servidor fora do ar ou falta de importação dos arquivos|

---

### Importação

`GET` - **/api/importacao/**

Exemplo de resposta:

```json
    [
        {
            "pais": "Africa do Sul",
            "ano": 1970,
            "quantidade": 0,
            "valor": 0.0,
            "id": 1
        },
        {
            "pais": "Alemanha",
            "ano": 1970,
            "quantidade": 52297,
            "valor": 30498.0,
            "id": 2
        },
            ...
    ]
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os dados foram retornados com sucesso.|
|500     | Servidor fora do ar ou falta de importação dos arquivos|

---

### Processamento

`GET` - **/api/processamento/**

Exemplo de resposta:

```json
    [
        {
            "cultivar": "Alicante Bouschet",
            "ano": 1970,
            "quantidade": 0,
            "tipo": "TINTAS",
            "id": 2
        },
        {
            "cultivar": "Ancelota",
            "ano": 1970,
            "quantidade": 0,
            "tipo": "TINTAS",
            "id": 3
        },
            ...
    ]
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os dados foram retornados com sucesso.|
|500     | Servidor fora do ar ou falta de importação dos arquivos|

---

### Produção

`GET` - **/api/producao/**

Exemplo de resposta:

```json
    [
        {
            "produto": "Tinto",
            "ano": 1970,
            "litros": 174224052,
            "tipo": "VINHO DE MESA",
            "id": 2
        },
        {
            "produto": "Branco",
            "ano": 1970,
            "litros": 748400,
            "tipo": "VINHO DE MESA",
            "id": 3
        },
            ...
    ]
```

Códigos da Resposta

| Código | Descrição                            |
|--------|--------------------------------------|
|200     | Os dados foram retornados com sucesso.|
|500     | Servidor fora do ar ou falta de importação dos arquivos|