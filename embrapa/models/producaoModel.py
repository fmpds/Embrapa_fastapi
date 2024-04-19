from sqlalchemy import Column, Integer, String

from embrapa.database import Base


class Producao(Base):
    __tablename__ = 'producao'

    id = Column(Integer, primary_key=True)
    produto = Column(String(100), nullable=False)
    ano = Column(Integer)
    litros = Column(Integer)
    tipo = Column(String(100), nullable=False)