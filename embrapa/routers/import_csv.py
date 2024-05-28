import time
from fastapi import APIRouter, Depends
from embrapa.import_embrapa import import_embrapa
from embrapa.repository.authRepository import authorize_user
import embrapa.database as database


router = APIRouter(dependencies=[Depends(authorize_user)])


async def get_db():
    async with database.SessionLocal() as session:
        yield session


@router.get('/api/importar_csv_site_embrapa')
def importa_csv(
    online: bool = False,
    description='Define se a importação será online ou offline',
):
    try:
        import_embrapa.import_csv_site_embrapa(online)
        return 'Arquivos CSVs importados com sucesso do site da Embrapa!'
    except TimeoutError:
        # Tratamento para tempo limite
        time.sleep(5)  # Espera 5 segundos e tenta novamente
        import_embrapa.import_csv_site_embrapa(online)
        return 'Tentativa de importação de arquivos CSVs no site da EMBRAPA excedeu o tempo limite!'
