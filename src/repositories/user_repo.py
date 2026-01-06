import json
import os
from src.models.user import User
from typing import List, Optional

DATA_PATH = "data/users.json"


class UserJsonRepo:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_PATH):
            with open(DATA_PATH, "w") as f:
                json.dump([], f)

    def _read(self) -> List[dict]:
        with open(DATA_PATH, "r") as f:
            if os.stat(DATA_PATH).st_size == 0:
                return []
            return json.load(f)

    def _save(self, data: List[dict]):
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def create(self, user: User) -> User:
        db = self._read()
        db.append(user.model_dump())
        self._save(db)
        return user

    def get_by_mail(self, email: str) -> Optional[User]:
        db = self._read()
        for user in db:
            if user["email"] == email:
                return User(**user)
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        db = self._read()
        for user in db:
            if user["username"] == username:
                return User(**user)
        return None
