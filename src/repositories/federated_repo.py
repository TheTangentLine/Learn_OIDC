from ..models.federated import Federated

class FederatedRepo:
    async def create(self, federated: Federated):
        await federated.insert()
        return federated
    async def check_unique(self, provider: str, sub: str):
        federated = await Federated.find_one(Federated.provider == provider and Federated.subject_id == sub)
        return federated != None
