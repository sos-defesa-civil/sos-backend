from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
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
    id: int

class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    oc_id: int

    class Config:
        from_attributes = True