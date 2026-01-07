from jose import jwt
import os
from datetime import datetime, timedelta, timezone
import uuid
from fastapi import HTTPException, status
from dotenv import load_dotenv
from passlib.context import CryptContext

from src.models.user import User
from src.models.refresh_token import RefreshToken
from src.dtos.login_dto import LoginInputDto, LoginResponseDto, TokenResponseDto
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.repositories.user_repo import UserRepo
from src.repositories.token_repo import TokenRepo

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_TTL = int(os.getenv("ACCESS_TOKEN_TTL"))
REFRESH_TOKEN_TTL = int(os.getenv("REFRESH_TOKEN_TTL"))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, ttl: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ttl)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None


class AuthService:
    def __init__(self, user_repo: UserRepo, token_repo: TokenRepo):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def signUp(self, user: SignUpInputDto) -> SignUpResponseDto:
        if await self.user_repo.get_by_mail(user.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        new_user = User(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
        )
        created_user = await self.user_repo.create(new_user)
        return SignUpResponseDto.model_validate(created_user)

    async def login(self, user: LoginInputDto) -> TokenResponseDto:
        find_user = await self.user_repo.get_by_username(user.username)
        if not find_user or not verify_password(user.password, find_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        user_id = str(find_user.id)
        access_token = create_token(data={"sub": user_id}, ttl=ACCESS_TOKEN_TTL)
        refresh_token = create_token(data={"sub": user_id}, ttl=REFRESH_TOKEN_TTL)

        new_refresh_token = RefreshToken(
            token=refresh_token,
            user_id=find_user.id,
            expires_at=datetime.now(timezone.utc)
            + timedelta(minutes=REFRESH_TOKEN_TTL),
        )
        await self.token_repo.create(new_refresh_token)
        return TokenResponseDto(access_token=access_token, refresh_token=refresh_token)

    async def renew_access_token(self, refresh_token: str) -> LoginResponseDto:
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token content")
        valid_token = await self.token_repo.get_valid_token(refresh_token)
        if not valid_token:
            raise HTTPException(
                status_code=401, detail="Refresh token has been revoked or not found"
            )
        new_access_token = create_token(data={"sub": user_id}, ttl=ACCESS_TOKEN_TTL)

        return LoginResponseDto(access_token=new_access_token)
