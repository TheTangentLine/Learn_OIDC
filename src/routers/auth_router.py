from fastapi import APIRouter, Depends, Body, Response
from src.dtos.login_dto import LoginInputDto, LoginResponseDto
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.repositories.user_repo import UserRepo
from src.repositories.token_repo import TokenRepo
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service():
    repo = UserRepo()
    token_repo = TokenRepo()
    return AuthService(user_repo=repo, token_repo=token_repo)


@router.post("/signup", response_model=SignUpResponseDto)
async def sign_up(
    user: SignUpInputDto, service: AuthService = Depends(get_auth_service)
):
    return await service.signUp(user)


@router.post("/login", response_model=LoginResponseDto)
async def login(
    user: LoginInputDto,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.login(user)
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
        secure=False,
        path="/",
    )
    return LoginResponseDto(access_token=result.access_token)


@router.post("/refresh", response_model=LoginResponseDto)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    service: AuthService = Depends(get_auth_service),
):
    return await service.renew_access_token(refresh_token)


@router.get("/login/google")
def login_google():
    pass
