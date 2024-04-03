from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = 'sqlite+aiosqlite:///./mle.db'
DATABASE_URL = 'sqlite+aiosqlite:///./db.sqlite3'


engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()
