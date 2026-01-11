from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from ..core.third_party.oauth_client import google_auth
from ..repositories.user_repo import UserRepo
from ..repositories.federated_repo import FederatedRepo
from src.repositories.token_repo import TokenRepo
from ..models.user import User
from ..models.federated import Federated
from src.models.refresh_token import RefreshToken
from src.dtos.token_dto import TokenResponseDto
from src.core.security import *

import uuid


class ThirdPartyAuthService:
    def __init__(
        self, user_repo: UserRepo, federated_repo: FederatedRepo, token_repo: TokenRepo
    ):
        self.user_repo = user_repo
        self.federated_repo = federated_repo
        self.token_repo = token_repo

    async def google_login(self, request: Request):
        redirect_uri = request.url_for("google_callback")
        return await google_auth.google.authorize_redirect(request, redirect_uri)  # type: ignore

    async def google_callback(self, request: Request) -> TokenResponseDto:
        token = await google_auth.google.authorize_access_token(request)  # type: ignore

        user_info = token.get("userinfo")
        email = user_info.get("email")
        is_verified = user_info.get("email_verified")
        sub = user_info.get("sub")

        if not email or not is_verified:
            raise HTTPException(status_code=400, detail="No email found in token")

        user = await self.user_repo.get_by_mail(email)

        if user:
            existing_link = await self.federated_repo.check_unique("google", sub)
            if not existing_link:
                new_link = Federated(
                    user_id=str(user.id), provider="google", subject_id=sub
                )
                await self.federated_repo.create(new_link)
            # return JSONResponse(status_code=status.HTTP_200_OK, content={"email": email, "message": "login successfully"})

        else:
            new_user = User(
                username=str(uuid.uuid4()),
                email=email,
            )
            user = await self.user_repo.create(new_user)

            federated = Federated(
                user_id=str(user.id), provider="google", subject_id=sub
            )

            await self.federated_repo.create(federated)

        user_id = str(user.id)
        access_token = create_access_token(TokenSub(user_id))
        refresh_token = create_refresh_token()

        new_refresh_token = RefreshToken(
            token=refresh_token,
            user_id=user.id,  # type: ignore
            expires_at=datetime.now(timezone.utc)
            + timedelta(minutes=settings.REFRESH_TOKEN_TTL),
        )

        await self.token_repo.create(new_refresh_token)
        return TokenResponseDto(access_token=access_token, refresh_token=refresh_token)

        # return JSONResponse(status_code=status.HTTP_201_CREATED, content={"email": email, "message": "create user successfully"})
