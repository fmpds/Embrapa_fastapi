from sqlalchemy.orm import declarative_base, sessionmaker
from embrapa.config import settings
from sqlalchemy import create_engine
# DATABASE_URL = 'sqlite+aiosqlite:///./mle.db'
# DATABASE_URL = 'sqlite+aiosqlite:///./db.sqlite3'


engine = create_engine(settings.database_uri, echo=True)

SessionLocal = sessionmaker(
    engine, expire_on_commit=False
)

Base = declarative_base()
