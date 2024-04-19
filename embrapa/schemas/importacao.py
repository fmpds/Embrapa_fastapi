from pydantic import BaseModel, Field


class ImportacaoBase(BaseModel):
    PAIS: str = Field(...)
    ANO: int = Field(...)
    QUANTIDADE: int = Field(...)
    VALOR: float = Field(...)

class ImportacaoCreate(ImportacaoBase):
    pass


class Importacao(ImportacaoBase):
    ID: str
    class Config:
        from_attributes = True
