from pydantic import BaseModel, ConfigDict

class LoginInputDto(BaseModel):
    username: str
    password: str

class LoginResponseDto(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)
