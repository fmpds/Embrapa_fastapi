from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.producaoModel import Producao


async def get_producoes(db: AsyncSession):
    result = await db.execute(select(Producao))
    return result.scalars().all()
