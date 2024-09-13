from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MidiaBase(BaseModel):
    id: int
    tipo: str
    caminho: str
    oc_id: int

    class Config:
        orm_mode = True

class MidiaCreate(MidiaBase):
    pass

class MidiaUpdate(MidiaBase):
    pass