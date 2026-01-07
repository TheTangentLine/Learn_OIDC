from src.models.user import User
from typing import Optional


class UserRepo:
    async def create(self, user: User) -> User:
        await user.insert()
        return user
    
    async def check_unique(self, email: str, username: str) -> bool:
        user = await User.find_one(User.email == email or User.username == username)
        return user != None

    async def get_by_mail(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await User.find_one(User.username == username)
