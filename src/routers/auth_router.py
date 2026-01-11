from fastapi import APIRouter, Depends, Response, Cookie, Request, status
from fastapi.responses import RedirectResponse
from src.dtos.login_dto import LoginInputDto, LoginResponseDto
from src.dtos.signup_dto import SignUpInputDto, SignUpResponseDto
from src.services.auth_service import AuthService
from src.services.third_party_auth_service import ThirdPartyAuthService
from src.core.dependency_injection import get_auth_service, get_third_party_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

# --------------------------- Sign up -------------------------->

@router.post("/signup", response_model=SignUpResponseDto,  status_code=status.HTTP_201_CREATED)
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
async def login_google(
    request: Request,
    service: ThirdPartyAuthService = Depends(get_third_party_auth_service)
):
    return await service.google_login(request)

@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    service: ThirdPartyAuthService = Depends(get_third_party_auth_service),
):
    result = await service.google_callback(request)
    frontend_url = "http://localhost:3000/login-success"
    response = RedirectResponse(url=f"{frontend_url}?access_token={result.access_token}")
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
        secure=False,
        path="/",
    )
    return response
