from fastapi import APIRouter, Depends, Response, Cookie
from src.dtos.login_dto import LoginInputDto, LoginResponseDto
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.repositories.user_repo import UserRepo
from src.repositories.token_repo import TokenRepo
from src.services.auth_service import AuthService
from src.core.dependency_injection import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

# --------------------------- Sign up -------------------------->

@router.post("/signup", response_model=SignUpResponseDto)
async def sign_up(
    user: SignUpInputDto, 
    service: AuthService = Depends(get_auth_service)
):
    return await service.sign_up(user)

# --------------------------- Login -------------------------->

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

# --------------------------- Refresh ------------------------>

@router.post("/refresh", response_model=LoginResponseDto)
async def refresh_token(
    refresh_token: str | None = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
):
    return await service.renew_access_token(refresh_token)

# -------------------------- Third parties --------------------->

@router.get("/login/google")
def login_google():
    pass
