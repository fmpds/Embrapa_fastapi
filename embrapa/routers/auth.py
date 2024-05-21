from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from embrapa.schemas.auth import User, Token
from embrapa.repository.authRepository import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    create_user,
)
import embrapa.database as database

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    with database.SessionLocal() as session:
        yield session

@router.post('/user')
async def create_user_route(
        form_data: User,
        db: database.SessionLocal = Depends(get_db)
    ):

    user = create_user(form_data.username, form_data.password, form_data.email, form_data.full_name, db)

    return user

@router.post('/token')
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: database.SessionLocal = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)

    if user is None:
        raise HTTPException(
            status_code=400, detail='Incorrect username or password'
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me')
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
