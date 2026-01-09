
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TokenResponseDto(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)

class TokenSub(BaseModel):
    user_id: str
    exp: datetime = datetime.now()

    def __init__(self, user_id):
        super().__init__(user_id=user_id)

# New class: RefreshTokenDto (user id)