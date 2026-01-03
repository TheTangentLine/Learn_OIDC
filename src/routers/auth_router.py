from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def sign_up():
    pass

@router.post("/login")
def login():
    pass

@router.get("/login/google")
def login_google():
    pass