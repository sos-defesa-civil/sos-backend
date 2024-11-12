from pydantic import BaseModel
from datetime import datetime
from typing import List

class RegistroResponse(BaseModel):
    id: int
    user_id: int
    username: str
    data: datetime
    tipo: str
    descricao: str

    class Config:
        from_attributes = True
