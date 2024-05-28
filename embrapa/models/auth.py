from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from embrapa.database import Base


class Token(Base):
    __tablename__ = 'tokens'

    access_token = Column(String(100), primary_key=True)
    username = Column(String(100))


class TokenData(Base):
    __tablename__ = 'token_data'

    username = Column(String(100), primary_key=True)


class User(Base):
    __tablename__ = 'users'

    username = Column(String(100), primary_key=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    disabled = Column(Boolean, default=False)


class UserInDB(User):
    __tablename__ = 'users_in_db'

    username = Column(String(100), ForeignKey(User.username), primary_key=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
