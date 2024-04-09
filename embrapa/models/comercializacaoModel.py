from sqlalchemy import Column, Integer, String

from embrapa.database import Base


class Comercializacao(Base):
    __tablename__ = 'comercializacao'

    id = Column(Integer, primary_key=True)
    produto = Column(String(100), nullable=False)
    ano_1970 = Column('1970', Integer)
    ano_1971 = Column('1971', Integer)
    ano_1972 = Column('1972', Integer)
    ano_1973 = Column('1973', Integer)
    ano_1974 = Column('1974', Integer)
    ano_1975 = Column('1975', Integer)
    ano_1976 = Column('1976', Integer)
    ano_1977 = Column('1977', Integer)
    ano_1978 = Column('1978', Integer)
    ano_1979 = Column('1979', Integer)
    ano_1980 = Column('1980', Integer)
    ano_1981 = Column('1981', Integer)
    ano_1982 = Column('1982', Integer)
    ano_1983 = Column('1983', Integer)
    ano_1984 = Column('1984', Integer)
    ano_1985 = Column('1985', Integer)
    ano_1986 = Column('1986', Integer)
    ano_1987 = Column('1987', Integer)
    ano_1988 = Column('1988', Integer)
    ano_1989 = Column('1989', Integer)
    ano_1990 = Column('1990', Integer)
    ano_1991 = Column('1991', Integer)
    ano_1992 = Column('1992', Integer)
    ano_1993 = Column('1993', Integer)
    ano_1994 = Column('1994', Integer)
    ano_1995 = Column('1995', Integer)
    ano_1996 = Column('1996', Integer)
    ano_1997 = Column('1997', Integer)
    ano_1998 = Column('1998', Integer)
    ano_1999 = Column('1999', Integer)
    ano_2000 = Column('2000', Integer)
    ano_2001 = Column('2001', Integer)
    ano_2002 = Column('2002', Integer)
    ano_2003 = Column('2003', Integer)
    ano_2004 = Column('2004', Integer)
    ano_2005 = Column('2005', Integer)
    ano_2006 = Column('2006', Integer)
    ano_2007 = Column('2007', Integer)
    ano_2008 = Column('2008', Integer)
    ano_2009 = Column('2009', Integer)
    ano_2010 = Column('2010', Integer)
    ano_2011 = Column('2011', Integer)
    ano_2012 = Column('2012', Integer)
    ano_2013 = Column('2013', Integer)
    ano_2014 = Column('2014', Integer)
    ano_2015 = Column('2015', Integer)
    ano_2016 = Column('2016', Integer)
    ano_2017 = Column('2017', Integer)
    ano_2018 = Column('2018', Integer)
    ano_2019 = Column('2019', Integer)
    ano_2020 = Column('2020', Integer)
    ano_2021 = Column('2021', Integer)
    ano_2022 = Column('2022', Integer)