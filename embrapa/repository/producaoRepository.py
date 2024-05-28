from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.producaoModel import Producao


def get_producoes(db: AsyncSession):
    result = db.execute(select(Producao))
    return result.scalars().all()
