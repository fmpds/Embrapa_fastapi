from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from embrapa.routers import apis, import_csv, auth


app = FastAPI()
<<<<<<< HEAD

app.mount('/mkdocs', StaticFiles(directory='site', html=True), name='mkdocs')

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
=======
app.include_router(import_csv.router)
app.include_router(apis.router)
app.include_router(auth.router)
app.mount('/mkdocs', StaticFiles(directory='site', html=True), name='mkdocs')
>>>>>>> 90834444bce8a37fa45e37c956e167d826a8943d
