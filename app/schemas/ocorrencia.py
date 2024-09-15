from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude
from typing import Literal, Optional
from datetime import datetime

class OcorrenciaBase(BaseModel):
    #TODO configurar determinar todos os tipos
    tipo: Literal['tipo1', 'tipo2', 'tipo3'] 
    descricao: str
    data_registro: datetime
    ultima_atualizacao: Optional[datetime]
    user_id: int
    latitude: Latitude
    longitude: Longitude

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
