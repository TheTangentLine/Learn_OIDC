from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from ..dtos.token_dto import TokenSub
from .config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: TokenSub) -> str:
    data.exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_TTL)
    encoded_jwt = jwt.encode(data.model_dump(), settings.PUBLIC_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    payload = jwt.decode(token, settings.PRIVATE_KEY, algorithms=[settings.ALGORITHM])
    return payload

def create_refresh_token() -> str:
    return "hhelo world"

