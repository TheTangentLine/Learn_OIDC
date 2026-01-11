
from ..repositories.token_repo import TokenRepo
from ..repositories.user_repo import UserRepo
from ..repositories.federated_repo import FederatedRepo
from ..services.auth_service import AuthService
from ..services.third_party_auth_service import ThirdPartyAuthService

def get_auth_service():
    repo = UserRepo()
    token_repo = TokenRepo()
    return AuthService(user_repo=repo, token_repo=token_repo)

def get_third_party_auth_service():
    user_repo = UserRepo()
    federated_repo = FederatedRepo()
    token_repo = TokenRepo()
    return ThirdPartyAuthService(user_repo=user_repo, federated_repo=federated_repo, token_repo=token_repo)