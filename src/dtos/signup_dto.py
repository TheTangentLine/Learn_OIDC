from pydantic import BaseModel, ConfigDict, EmailStr
from beanie import PydanticObjectId


class SignUpInputDto(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignUpResponseDto(BaseModel):
    id: PydanticObjectId
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
