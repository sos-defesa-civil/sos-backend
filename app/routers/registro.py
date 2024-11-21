from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.registro import RegistroResponse
from app.repositories.registro import get_logs
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/registro", 
    response_model=List[RegistroResponse],
    summary="Obter registros de eventos",
    description=(
        "Esta rota retorna uma lista de registros de logs disponíveis no sistema. "
        "Os registros podem incluir informações de operações realizadas, alterações no sistema, "
        "ou eventos capturados automaticamente.\n\n"
    ),)
def get(db: Session = Depends(get_db)):
    return get_logs(db)
