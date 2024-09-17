from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.curtida import CurtidaResponse
from typing import Literal, Optional, List
from datetime import datetime

class OcorrenciaBase(BaseModel):
    #TODO configurar determinar todos os tipos
    tipo: Literal['tipo1', 'tipo2', 'tipo3'] 
    bairro: str
    descricao: str
    data_registro: datetime
    ultima_atualizacao: Optional[datetime]
    user_id: int
    latitude: Latitude
    longitude: Longitude

    class Config:
        from_attributes = True

class OcorrenciaCreate(OcorrenciaBase):
    pass

class OcorrenciaUpdate(OcorrenciaBase):
    pass


class OcorrenciaResponse(OcorrenciaBase):
    id: int
    curtidas_count: int

    class Config:
        from_attributes = True


class Bounds(BaseModel):
    ne_lat: Latitude
    ne_lng: Longitude
    sw_lat: Latitude
    sw_lng: Longitude

    class Config:
        from_attributes = True