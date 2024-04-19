from pydantic import BaseModel, Field


class ProcessamentoBase(BaseModel):
    CULTIVAR: str = Field(...)
    QUANTIDADE: int = Field(...)
    TIPO: str = Field(...)
    ANO: int = Field(...)


class ProcessamentoCreate(ProcessamentoBase):
    pass


class Processamento(ProcessamentoBase):
    ID: str
    class Config:
        from_attributes = True
