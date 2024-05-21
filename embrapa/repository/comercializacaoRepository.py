from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.comercializacaoModel import Comercializacao


def get_comercializacoes(db: AsyncSession):
    result = db.execute(select(Comercializacao))
    return result.scalars().all()
