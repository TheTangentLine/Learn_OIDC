from datetime import datetime
from beanie import Document, PydanticObjectId
from pydantic import Field
import pymongo
from pymongo import IndexModel


class RefreshToken(Document):
    token: str
    user_id: PydanticObjectId
    expires_at: datetime
    revoked: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "refresh_tokens"

        indexes = [
            "token",
            "user_id",
            IndexModel(
                [("expires_at", pymongo.ASCENDING)],
                expireAfterSeconds=0,
            ),
        ]
