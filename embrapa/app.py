import time
from typing import List

from fastapi import Depends, FastAPI, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from embrapa import database
from embrapa.import_embrapa import import_embrapa
from embrapa.repository import (
    comercializacaoRepository,
    exportacaoRepository,
    importacaoRepository,
    processamentoRepository,
    producaoRepository,
)
from embrapa.schemas.comercializacao import Comercializacao
from embrapa.schemas.exportacao import Exportacao
from embrapa.schemas.importacao import Importacao
from embrapa.schemas.processamento import Processamento
from embrapa.schemas.producao import Producao

app = FastAPI()

#app.mount('/mkdocs', StaticFiles(directory='site', html=True), name='mkdocs')

@app.get('/api/importar_csv_site_embrapa')
def importa_csv(online: bool = False, description="Define se a importação será online ou offline"):
    try:
        import_embrapa.import_csv_site_embrapa(online)
        return 'Arquivos CSVs importados com sucesso do site da Embrapa!'
    except TimeoutError:
        # Tratamento para tempo limite
        time.sleep(5)  # Espera 5 segundos e tenta novamente
        import_embrapa.import_csv_site_embrapa(online)
        return 'Tentativa de importação de arquivos CSVs no site da EMBRAPA excedeu o tempo limite!'


# Função para obter uma instância de sessão assíncrona do banco de dados
async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@app.get('/api/producao/', response_model=List[Producao])
async def get_producoes(db: database.AsyncSessionLocal = Depends(get_db)):
    producoes = await producaoRepository.get_producoes(db)
    return producoes


@app.get('/api/processamento/', response_model=List[Processamento])
async def get_procesamentos(db: database.AsyncSessionLocal = Depends(get_db)):
    processamentos = await processamentoRepository.get_processamentos(db)
    return processamentos


@app.get('/api/importacao/', response_model=List[Importacao])
async def get_importacoes(db: database.AsyncSessionLocal = Depends(get_db)):
    importacoes = await importacaoRepository.get_importacoes(db)
    return importacoes


@app.get('/api/exportacao/', response_model=List[Exportacao])
async def get_exportacoes(db: database.AsyncSessionLocal = Depends(get_db)):
    exportacoes = await exportacaoRepository.get_exportacoes(db)
    return exportacoes


@app.get('/api/comercializacao/', response_model=List[Comercializacao])
async def get_exportacoes(db: database.AsyncSessionLocal = Depends(get_db)):
    comercializacoes = await comercializacaoRepository.get_comercializacoes(db)
    return comercializacoes
