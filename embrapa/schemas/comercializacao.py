from pydantic import BaseModel, Field


class ComercializacaoBase(BaseModel):
    PRODUTO: str = Field(...)
    TIPO: str = Field(...)
    LITROS: int = Field(...)
    ANO: int = Field(...)
            
            
class ComercializacaoCreate(ComercializacaoBase):
    pass

class Comercializacao(ComercializacaoBase):
    ID: str
    class Config:
        from_attributes = True