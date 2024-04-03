from pydantic import BaseModel


class ProducaoBase(BaseModel):
    produto: str
    ano_1970: int
    ano_1971: int
    ano_1972: int
    ano_1973: int
    ano_1974: int
    ano_1975: int
    ano_1976: int
    ano_1977: int
    ano_1978: int
    ano_1979: int
    ano_1980: int
    ano_1981: int
    ano_1982: int
    ano_1983: int
    ano_1984: int
    ano_1985: int
    ano_1986: int
    ano_1987: int
    ano_1988: int
    ano_1989: int
    ano_1990: int
    ano_1991: int
    ano_1992: int
    ano_1993: int
    ano_1994: int
    ano_1995: int
    ano_1996: int
    ano_1997: int
    ano_1998: int
    ano_1999: int
    ano_2000: int
    ano_2001: int
    ano_2002: int
    ano_2003: int
    ano_2004: int
    ano_2005: int
    ano_2006: int
    ano_2007: int
    ano_2008: int
    ano_2009: int
    ano_2010: int
    ano_2011: int
    ano_2012: int
    ano_2013: int
    ano_2014: int
    ano_2015: int
    ano_2016: int
    ano_2017: int
    ano_2018: int
    ano_2019: int
    ano_2020: int
    ano_2021: int
    ano_2022: int


class ProducaoCreate(ProducaoBase):
    pass


class Producao(ProducaoBase):
    id: int

    class Config:
        from_attributes = True
