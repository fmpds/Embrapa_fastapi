from pydantic import BaseModel, Field


class ImportacaoBase(BaseModel):
    pais: str 
    ano: int 
    quantidade: int
    valor: float


class ImportacaoCreate(ImportacaoBase):
    pass


class Importacao(ImportacaoBase):
    id_x: int

    class Config:
        from_attributes = True
