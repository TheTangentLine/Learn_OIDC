from pydantic import BaseModel

class LoginInputDto(BaseModel):
    username: str
    password: str

class LoginResponseDto(BaseModel):
    access_token: str
    token_type: str = "bearer"