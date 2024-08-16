import os

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt # type: ignore
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from movie_app.logger import logger

from movie_app.crud import user_crud_service


UTC = timezone(offset=timedelta(0))
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY') 
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    logger.info('Password verified Successfully')
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = user_crud_service.get_user_by_username_with_hash(username)
    if not user or not verify_password(password, user.get('hashed_password')):
        logger.warning(f'User with {user.username} not authenticated')
        return False
    logger.info('User Successfully authenticated')
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        logger.exception(f'User credentials nor for {get_current_user} ')
        raise credentials_exception
    user = user_crud_service.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    logger.info('user gotten succesfully')
    return user

