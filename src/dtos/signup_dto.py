from pydantic import BaseModel, EmailStr

class SignUpInputDto(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignUpResponseDto(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attribute = True