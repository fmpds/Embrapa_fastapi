from sqlalchemy import Column, Integer, String

from embrapa.database import Base


class Comercializacao(Base):
    __tablename__ = 'comercializacao'

    id = Column(Integer, primary_key=True)
    produto = Column(String(100), nullable=False)
    ano = Column(Integer)
    litros = Column(Integer)
    tipo = Column(String(100), nullable=False)