from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CurtidaBase(BaseModel):
    id: int
    data_registro: datetime
    user_id: int
    oc_id: int

    class Config:
        from_attributes = True

class CurtidaCreate(CurtidaBase):
    pass