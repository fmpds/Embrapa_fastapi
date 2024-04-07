from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.comercializacaoModel import Comercializacao


async def get_comercializacoes(db: AsyncSession):
    result = await db.execute(select(Comercializacao))
    return result.scalars().all()
