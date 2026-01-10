from fastapi import Request, status
from fastapi.responses import JSONResponse

from ..core.third_party.oauth_client import google_auth
from ..repositories.user_repo import UserRepo
from ..repositories.federated_repo import FederatedRepo
from ..models.user import User
from ..models.federated import Federated

import uuid

class ThirdPartyAuthService:
    def __init__(self, user_repo: UserRepo, federated_repo: FederatedRepo):
        self.user_repo = user_repo
        self.federated_repo = federated_repo

    async def google_login(self, request: Request):
        redirect_uri = request.url_for('google_callback')
        return await google_auth.google.authorize_redirect(request, redirect_uri) # type: ignore 

    async def google_callback(self, request: Request):
        token = await google_auth.google.authorize_access_token(request) # type: ignore
        
        user_info = token.get('userinfo')
        email = user_info.get('email')
        sub = user_info.get('sub')
        
        if not email:
            return JSONResponse(status_code=400, content={"message": "No email found in token"})

        existing_user = await self.user_repo.get_by_mail(email)

        if existing_user:
            existing_link = await self.federated_repo.check_unique("google", sub)
            if not existing_link:
                new_link = Federated(
                    user_id=str(existing_user.id),
                    provider="google",
                    subject_id=sub
                )
                await self.federated_repo.create(new_link)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"email": email, "message": "login successfully"})
        
        else:
            new_user = User(
                username=str(uuid.uuid4()), 
                email=email,
            )
            await self.user_repo.create(new_user)

            federated = Federated(
                user_id=str(new_user.id),
                provider="google",
                subject_id=sub
            )

            await self.federated_repo.create(federated)

            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"email": email, "message": "create user successfully"})
            