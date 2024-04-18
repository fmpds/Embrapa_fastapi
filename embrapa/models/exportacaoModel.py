from sqlalchemy import Column, Float, Integer, String

from embrapa.database import Base


class Exportacao(Base):
    __tablename__ = 'exportacao'

    #id = Column(Integer, primary_key=True)
    pais = Column(String(100), nullable=False)
    ano = Column(Integer)
    quantidade = Column(Integer)
    valor = Column(Float)
    