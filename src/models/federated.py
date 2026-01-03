from pydantic import BaseModel

class Federated(BaseModel):
    id: str
    user_id: str
    provider: str
    subject_id: str