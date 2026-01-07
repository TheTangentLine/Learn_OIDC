from pydantic import BaseModel, ConfigDict


class LoginInputDto(BaseModel):
    username: str
    password: str


class TokenResponseDto(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class LoginResponseDto(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)
