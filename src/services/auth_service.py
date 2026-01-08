from fastapi import HTTPException, status

from src.models.user import User
from src.models.refresh_token import RefreshToken
from src.dtos.login_dto import LoginInputDto, LoginResponseDto
from src.dtos.token_dto import TokenResponseDto, TokenSub
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.repositories.user_repo import UserRepo
from src.repositories.token_repo import TokenRepo
from src.core.security import *
from src.core.config import settings


class AuthService:
    def __init__(self, user_repo: UserRepo, token_repo: TokenRepo):
        self.user_repo = user_repo
        self.token_repo = token_repo

    # ---------------------------------- Sign up -------------------------->

    async def sign_up(self, user: SignUpInputDto) -> SignUpResponseDto:
        if await self.user_repo.check_unique(user.email, user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        new_user = User(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
        )
        created_user = await self.user_repo.create(new_user)
        return SignUpResponseDto.model_validate(created_user)

    # --------------------------------- Login ---------------------------->

    async def login(self, user: LoginInputDto) -> TokenResponseDto:
        find_user = await self.user_repo.get_by_username(user.username)
        if not find_user or not verify_password(user.password, find_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user_id = str(find_user.id)
        access_token = create_access_token(TokenSub(user_id))
        refresh_token = create_refresh_token()

        new_refresh_token = RefreshToken(
            token=refresh_token,
            user_id=find_user.id,  # type: ignore
            expires_at=datetime.now(timezone.utc)
            + timedelta(minutes=settings.REFRESH_TOKEN_TTL),
        )

        await self.token_repo.create(new_refresh_token)
        return TokenResponseDto(access_token=access_token, refresh_token=refresh_token)

    # -------------------------------- Refresh token ----------------------->

    async def renew_access_token(self, refresh_token: str | None) -> LoginResponseDto:

        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        valid_token = await self.token_repo.get_valid_token(refresh_token)
        if not valid_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        user_id = valid_token.user_id
        new_access_token = create_access_token(TokenSub(user_id))

        return LoginResponseDto(access_token=new_access_token)
