from pydantic import BaseModel


class ComercializacaoBase(BaseModel):
    produto: str
    ano: int
    litros: int
    tipo: str


class ComercializacaoCreate(ComercializacaoBase):
    pass


class Comercializacao(ComercializacaoBase):
    id: int

    class Config:
        from_attributes = True
