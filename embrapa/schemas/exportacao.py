from pydantic import BaseModel


class ExportacaoBase(BaseModel):
    pais: str
    quantidade_1970: int
    valor_1970: int
    quantidade_1971: int
    valor_1971: int
    quantidade_1972: int
    valor_1972: int
    quantidade_1973: int
    valor_1973: int
    quantidade_1974: int
    valor_1974: int
    quantidade_1975: int
    valor_1975: int
    quantidade_1976: int
    valor_1976: int
    quantidade_1977: int
    valor_1977: int
    quantidade_1978: int
    valor_1978: int
    quantidade_1979: int
    valor_1979: int
    quantidade_1980: int
    valor_1980: int
    quantidade_1981: int
    valor_1981: int
    quantidade_1982: int
    valor_1982: int
    quantidade_1983: int
    valor_1983: int
    quantidade_1984: int
    valor_1984: int
    quantidade_1985: int
    valor_1985: int
    quantidade_1986: int
    valor_1986: int
    quantidade_1987: int
    valor_1987: int
    quantidade_1988: int
    valor_1988: int
    quantidade_1989: int
    valor_1989: int
    quantidade_1990: int
    valor_1990: int
    quantidade_1991: int
    valor_1991: int
    quantidade_1992: int
    valor_1992: int
    quantidade_1993: int
    valor_1993: int
    quantidade_1994: int
    valor_1994: int
    quantidade_1995: int
    valor_1995: int
    quantidade_1996: int
    valor_1996: int
    quantidade_1997: int
    valor_1997: int
    quantidade_1998: int
    valor_1998: int
    quantidade_1999: int
    valor_1999: int
    quantidade_2000: int
    valor_2000: int
    quantidade_2001: int
    valor_2001: int
    quantidade_2002: int
    valor_2002: int
    quantidade_2003: int
    valor_2003: int
    quantidade_2004: int
    valor_2004: int
    quantidade_2005: int
    valor_2005: int
    quantidade_2006: int
    valor_2006: int
    quantidade_2007: int
    valor_2007: int
    quantidade_2008: int
    valor_2008: int
    quantidade_2009: int
    valor_2009: int
    quantidade_2010: int
    valor_2010: int
    quantidade_2011: int
    valor_2011: int
    quantidade_2012: int
    valor_2012: int
    quantidade_2013: int
    valor_2013: int
    quantidade_2014: int
    valor_2014: int
    quantidade_2015: int
    valor_2015: int
    quantidade_2016: int
    valor_2016: int
    quantidade_2017: int
    valor_2017: int
    quantidade_2018: int
    valor_2018: int
    quantidade_2019: int
    valor_2019: int
    quantidade_2020: int
    valor_2020: int
    quantidade_2021: int
    valor_2021: int
    quantidade_2022: int


class ExportacaoCreate(ExportacaoBase):
    pass


class Exportacao(ExportacaoBase):
    id: int

    class Config:
        from_attributes = True