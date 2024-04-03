from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.exportacaoModel import Exportacao


async def get_exportacoes(db: AsyncSession):
    result = await db.execute(select(Exportacao))
    return result.scalars().all()
