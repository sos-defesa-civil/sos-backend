from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.dashboard import CardResponse, PieChartResponse, MonthlyPieChartResponse
from app.cruds.dashboard import get_ocorrencia_data, get_curtida_data, count_ocorrencias_by_tipo, count_ocorrencias_by_tipo_per_month
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/dashboard/ocorrencias-card", response_model=CardResponse)
def ocorrencias_card(db: Session = Depends(get_db)):
    return get_ocorrencia_data(db)

@router.get("/dashboard/curtidas-card", response_model=CardResponse)
def curtidas_card(db: Session = Depends(get_db)):
    return get_curtida_data(db)
@router.get("/dashboard/pie-chart", response_model=PieChartResponse)
def pie_chart(db: Session = Depends(get_db)):
    return count_ocorrencias_by_tipo(db)

@router.get("/dashboard/monthly-chart", response_model=MonthlyPieChartResponse)
def monthly_chart(db: Session = Depends(get_db)):
    return count_ocorrencias_by_tipo_per_month(db);