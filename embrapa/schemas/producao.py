from pydantic import BaseModel, Field


class ProducaoBase(BaseModel):
    PRODUTO: str = Field(...)
    ANO: int = Field(...)
    LITROS: int = Field(...)
    TIPO: str = Field(...)

class ProducaoCreate(ProducaoBase):
    pass

class Producao(ProducaoBase):
    ID: str
    class Config:
        from_attributes = True
