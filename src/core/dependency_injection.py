
from ..repositories.token_repo import TokenRepo
from ..repositories.user_repo import UserRepo
from ..services.auth_service import AuthService

def get_auth_service():
    repo = UserRepo()
    token_repo = TokenRepo()
    return AuthService(user_repo=repo, token_repo=token_repo)