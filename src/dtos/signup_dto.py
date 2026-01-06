from pydantic import BaseModel, EmailStr, ConfigDict


class SignUpInputDto(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignUpResponseDto(BaseModel):
    id: str
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
