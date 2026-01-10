from beanie import Document

class Federated(Document):
    user_id: str
    provider: str
    subject_id: str