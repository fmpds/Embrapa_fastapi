from pydantic import BaseModel, Field


class ComercializacaoBase(BaseModel):
    PRODUTO: str
    TIPO: str
    LITROS: int
    ANO: int
            
class ComercializacaoCreate(ComercializacaoBase):
    pass

class Comercializacao(ComercializacaoBase):
    ID: str
    class Config:
        from_attributes = True