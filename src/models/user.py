from beanie import Document
from pymongo import IndexModel, ASCENDING


class User(Document):
    username: str
    email: str
    password: str = ""

    class Settings:
        name = "users"

        indexes = [
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("email", ASCENDING)], unique=True),
        ]
