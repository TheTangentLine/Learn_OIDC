from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .models.user import User
from .models.refresh_token import RefreshToken
from .models.federated import Federated

from .core.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        database=client[settings.DB_NAME],  # type: ignore
        document_models=[
            User, 
            RefreshToken, 
            Federated
        ]
    )
