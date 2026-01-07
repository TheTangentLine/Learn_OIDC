from jose import jwt
import os
from datetime import datetime, timedelta, timezone
import uuid
from fastapi import HTTPException, status
from dotenv import load_dotenv

from src.models.user import User
from src.dtos.login_dto import LoginInputDto, LoginResponseDto
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.repositories.user_repo import UserJsonRepo

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_TTL = int(os.getenv("ACCESS_TOKEN_TTL"))
REFRESH_TOKEN_TTL = int(os.getenv("REFRESH_TOKEN_TTL"))


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
    def __init__(self, user_repo: UserJsonRepo):
        self.user_repo = user_repo

    def signUp(self, user: SignUpInputDto) -> SignUpResponseDto:
        if self.user_repo.get_by_mail(user.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        new_user = User(
            id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            password=user.password,
        )
        created_user = self.user_repo.create(new_user)
        return SignUpResponseDto.model_validate(created_user)

    def login(self, user: LoginInputDto) -> LoginResponseDto:
        find_user = self.user_repo.get_by_username(user.username)
        if not find_user or find_user.password != user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = create_token(data={"sub": find_user.id}, ttl=ACCESS_TOKEN_TTL)
        refresh_token = create_token(data={"sub": find_user.id}, ttl=REFRESH_TOKEN_TTL)
        return LoginResponseDto(access_token=access_token, refresh_token=refresh_token)

    def renew_access_token(self, refresh_token: str) -> LoginResponseDto:
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        id = payload.get("sub")
        if not id:
            raise HTTPException(status_code=401, detail="Invalid token content")
        new_access_token = create_token(data={"sub": id}, ttl=ACCESS_TOKEN_TTL)
        return LoginResponseDto(
            access_token=new_access_token, refresh_token=refresh_token
        )
