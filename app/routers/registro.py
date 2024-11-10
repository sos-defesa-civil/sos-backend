from fastapi import APIRouter, Depends
from app.database import get_db
from app.schemas.registro import RegistroResponse
from app.models.registro import Registro
from app.cruds.registro import get_logs
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/registro", response_model=List[RegistroResponse])
def get(db: Session = Depends(get_db)):
    return get_logs(db)
