from pydantic import BaseModel
from datetime import datetime

class RegistroResponse(BaseModel):
    id: int
    user_id: int
    data: datetime
    tipo: str
    descricao: str

    class Config:
        from_attributes = True
