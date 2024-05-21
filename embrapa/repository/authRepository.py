from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, api_key
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.future import select

from embrapa import database
from embrapa.config import settings
from embrapa.models.auth import TokenData, User, UserInDB
from sqlalchemy.orm import Session

api_key_header = api_key.APIKeyHeader(name='ApiKey', auto_error=False)

SECRET_KEY = '96a1f42d3d5f92dd8c2df1d1f8396df052b9f163f43b6a8343601b6b06b55af7'
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    with database.SessionLocal() as session:
        yield session


def validate_api_key(key: str = Security(api_key_header)):
    if key != settings.api_key:
        raise HTTPException(status_code=403, detail='Invalid API Key')
    return True


def get_user(username: str, db: Session):
    try:
        result = db.execute(select(UserInDB).filter().where(UserInDB.username == username))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    user_dict = result.scalars().one()

    return user_dict


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        if token is None:
            return False
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user and current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


async def authorize_user(
    user: Annotated[str, Depends(get_current_active_user)],
    api_key: str = Security(api_key_header),
):
    if api_key and validate_api_key(api_key):
        return True  # Authorized by API key

    # If API key is not provided or not valid, validate the user via token
    if user:
        return True  # Authorized by user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized'
    )


def create_user(username: str, password: str, email: str, full_name: str, session: Session):
    hashed_password = get_password_hash(password)
    user_in_db = UserInDB(username=username, email=email, full_name=full_name, hashed_password=hashed_password)
    try:
        session.add(user_in_db)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user_in_db
