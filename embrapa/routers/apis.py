from typing import List

from fastapi import APIRouter, Depends

from embrapa import database
from embrapa.repository import (
    comercializacaoRepository,
    exportacaoRepository,
    importacaoRepository,
    processamentoRepository,
    producaoRepository,
)
from embrapa.repository.authRepository import authorize_user
from embrapa.schemas.comercializacao import Comercializacao
from embrapa.schemas.exportacao import Exportacao
from embrapa.schemas.importacao import Importacao
from embrapa.schemas.processamento import Processamento
from embrapa.schemas.producao import Producao

router = APIRouter(dependencies=[Depends(authorize_user)])


# Função para obter uma instância de sessão assíncrona do banco de dados
def get_db():
     with database.SessionLocal() as session:
        yield session


@router.get('/api/producao/', response_model=List[Producao])
def get_producoes(db: database.SessionLocal = Depends(get_db)):
    producoes = producaoRepository.get_producoes(db)
    return producoes


@router.get('/api/processamento/', response_model=List[Processamento])
def get_procesamentos(db: database.SessionLocal = Depends(get_db)):
    processamentos = processamentoRepository.get_processamentos(db)
    return processamentos


@router.get('/api/importacao/', response_model=List[Importacao])
def get_importacoes(db: database.SessionLocal = Depends(get_db)):
    importacoes = importacaoRepository.get_importacoes(db)
    return importacoes


@router.get('/api/exportacao/', response_model=List[Exportacao])
def get_exportacoes(db: database.SessionLocal = Depends(get_db)):
    exportacoes = exportacaoRepository.get_exportacoes(db)
    return exportacoes


@router.get('/api/comercializacao/', response_model=List[Comercializacao])
def get_exportacoes(db: database.SessionLocal = Depends(get_db)):
    comercializacoes = comercializacaoRepository.get_comercializacoes(db)
    return comercializacoes
