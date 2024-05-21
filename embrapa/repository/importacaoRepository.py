from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.importacaoModel import Importacao


def get_importacoes(db: AsyncSession):
    result = db.execute(select(Importacao))
    return result.scalars().all()
