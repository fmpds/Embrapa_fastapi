from sqlalchemy import Column, Integer, String

from embrapa.database import Base


class Comercializacao(Base):
    __tablename__ = 'comercializacao'

    ID = Column(Integer, primary_key=True)
    PRODUTO = Column(String(100), nullable=False)
    ANO = Column(Integer)
    LITROS = Column(Integer)
    TIPO = Column(String(100), nullable=False)