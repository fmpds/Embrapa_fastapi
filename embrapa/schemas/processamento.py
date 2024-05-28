from pydantic import BaseModel, Field


class ProcessamentoBase(BaseModel):
    cultivar: str
    ano: int
    quantidade: int
    tipo: str


class ProcessamentoCreate(ProcessamentoBase):
    pass


class Processamento(ProcessamentoBase):
    id: int

    class Config:
        from_attributes = True
