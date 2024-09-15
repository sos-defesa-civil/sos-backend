from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.cruds.ocorrencia import create_ocorrencia, get_ocorrencias, get_ocorrencia, update_ocorrencia, delete_ocorrencia
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ocorrencia/", response_model=OcorrenciaResponse)
def create_ocorrencia_route(ocorrencia: OcorrenciaCreate, db: Session = Depends(get_db)):
    return create_ocorrencia(db, ocorrencia) 

@router.get("/ocorrencia/", response_model=List[OcorrenciaResponse])
def read_ocorrencias_route(db: Session = Depends(get_db)):
    return get_ocorrencias(db)

@router.get("/ocorrencia/{ocorrencia_id}", response_model=OcorrenciaResponse)
def read_ocorrencia_route(ocorrencia_id: int, db: Session = Depends(get_db)):
    db_ocorrencia = get_ocorrencia(db, ocorrencia_id)
    if db_ocorrencia is None:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return db_ocorrencia

@router.put("/ocorrencia/{ocorrencia_id}", response_model=OcorrenciaResponse)
def update_ocorrencia_route(ocorrencia_id: int, ocorrencia: OcorrenciaCreate, db: Session = Depends(get_db)):
    db_ocorrencia = update_ocorrencia(db, ocorrencia_id, **ocorrencia.dict())
    if db_ocorrencia is None:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return db_ocorrencia

@router.delete("/ocorrencia/{ocorrencia_id}", response_model=OcorrenciaResponse)
def delete_ocorrencia_route(ocorrencia_id: int, db: Session = Depends(get_db)):
    db_ocorrencia = delete_ocorrencia(db, ocorrencia_id)
    if db_ocorrencia is None:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return db_ocorrencia
