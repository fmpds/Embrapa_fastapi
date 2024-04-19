from sqlalchemy import Column, Integer, String

from embrapa.database import Base


class Processamento(Base):
    __tablename__ = 'processamento'

    id = Column(Integer, primary_key=True)
    control = Column(String(50), nullable=False)
    cultivar = Column(String(50), nullable=False)
    ano = Column(Integer)
    