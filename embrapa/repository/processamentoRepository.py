from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from embrapa.models.processamentoModel import Processamento


async def get_processamentos(db: AsyncSession):
    result = await db.execute(select(Processamento))
    return result.scalars().all()
