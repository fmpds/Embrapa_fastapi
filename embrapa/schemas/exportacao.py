from pydantic import BaseModel, Field


class ExportacaoBase(BaseModel):
    PAIS: str = Field(...)
    ANO: int = Field(...)
    QUANTIDADE:int = Field(...)
    VALOR:float = Field(...)


class ExportacaoCreate(ExportacaoBase):
    pass


class Exportacao(ExportacaoBase):
    ID: str
    class Config:
        from_attributes = True
