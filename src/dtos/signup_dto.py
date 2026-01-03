from pydantic import BaseModel

class SignUpDto(BaseModel):
    username: str
    email: str
    password: str