from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OcorrenciaBase(BaseModel):
    id: int
    tipo: str
    descricao: str
    data_registro: datetime
    ultima_atualizacao: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True

class OcorrenciaCreate(OcorrenciaBase):
    pass

class OcorrenciaUpdate(OcorrenciaBase):
    pass


class OcorrenciaResponse(OcorrenciaBase):
    id: int

    class Config:
        from_attributes = True
