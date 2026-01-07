from fastapi import APIRouter, Depends, Body
from src.dtos.login_dto import LoginInputDto, LoginResponseDto
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.repositories.user_repo import UserJsonRepo
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service():
    repo = UserJsonRepo()
    return AuthService(repo)


@router.post("/signup", response_model=SignUpResponseDto)
def sign_up(user: SignUpInputDto, service: AuthService = Depends(get_auth_service)):
    return service.signUp(user)


@router.post("/login", response_model=LoginResponseDto)
def login(user: LoginInputDto, service: AuthService = Depends(get_auth_service)):
    return service.login(user)


@router.post("/refresh", response_model=LoginResponseDto)
def refresh_token(
    refresh_token: str = Body(..., embed=True),
    service: AuthService = Depends(get_auth_service),
):
    return service.renew_access_token(refresh_token)


@router.get("/login/google")
def login_google():
    pass
