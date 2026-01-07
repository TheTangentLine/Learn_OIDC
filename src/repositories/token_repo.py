from typing import Optional
from beanie import PydanticObjectId
from src.models.refresh_token import RefreshToken


class TokenRepo:
    async def create(self, token: RefreshToken) -> RefreshToken:
        await token.insert()
        return token

    async def get_valid_token(self, token_str: str) -> Optional[RefreshToken]:
        return await RefreshToken.find_one(
            RefreshToken.token == token_str, RefreshToken.revoked == False
        )

    async def revoke(self, token_str: str) -> None:
        await RefreshToken.find(RefreshToken.token == token_str).update(
            {"$set": {RefreshToken.revoked: True}}
        )
