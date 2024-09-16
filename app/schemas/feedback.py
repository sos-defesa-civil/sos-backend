from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str
    data_registro: datetime
    user_id: int
    oc_id: int

    class Config:
        orm_from_attributesmode = True

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(FeedbackBase):
    pass