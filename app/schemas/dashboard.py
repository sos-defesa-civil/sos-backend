from pydantic import BaseModel
from typing import List

class CardResponse(BaseModel):
    total: int
    today: int
    yesterdayPercent: float  
    lastWeekPercent: float  

class TipoCount(BaseModel):
    tipo: str
    count: int

class PieChartResponse(BaseModel):
    data: List[TipoCount]

class MonthlyTipoCount(BaseModel):
    tipo: str
    year: int
    month: int
    count: int

class MonthlyPieChartResponse(BaseModel):
    data: List[MonthlyTipoCount]

