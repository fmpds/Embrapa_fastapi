from pydantic import BaseModel, Field


class ExportacaoBase(BaseModel):
    pais: str
    ano: int 
    quantidade: int 
    valor: float 


class ExportacaoCreate(ExportacaoBase):
    pass


class Exportacao(ExportacaoBase):
    id: int

    class Config:
        from_attributes = True
