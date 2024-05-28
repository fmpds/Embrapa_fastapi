from pydantic import BaseModel, Field


class ProducaoBase(BaseModel):
    produto: str
    ano: int
    litros: int
    tipo: str


class ProducaoCreate(ProducaoBase):
    pass


class Producao(ProducaoBase):
    id: int

    class Config:
        from_attributes = True
