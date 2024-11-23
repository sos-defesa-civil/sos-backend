from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.curtida import CurtidaResponse
from typing import Literal, Optional, List
from datetime import datetime
from app.schemas.feedback import FeedbackResponse

class OcorrenciaBase(BaseModel):
    tipo: Literal['alagamentos', 'colapso_barragens', 'colapso_edificios', 'colapso_solo', 'deslizamentos',
                  'enxurradas', 'erosao_costeira', 'erosao_margem_fluvial', 'inundacoes', 'liberacao_quimicos',
                  'tempestade_raios', 'tombamentos_rolamentos', 'tremor_terra'] 
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
    username: str
    status: Optional[str] = "open"
    curtidas_count: Optional[int] = 0
    midias_count: Optional[int] = 0
    midias: Optional[List[str]] = []
    feedbacks: Optional[List[FeedbackResponse]] = []

    class Config:
        from_attributes = True

class OcorrenciaUpdateResponse(OcorrenciaBase):
    id: int

class OcorrenciaListResponse(BaseModel):
    results: List[OcorrenciaResponse]
    count: int


class Bounds(BaseModel):
    ne_lat: Latitude
    ne_lng: Longitude
    sw_lat: Latitude
    sw_lng: Longitude

    class Config:
        from_attributes = True
