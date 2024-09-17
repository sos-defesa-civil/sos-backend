from fastapi import APIRouter, File, HTTPException, Depends, Query, UploadFile
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.cruds.ocorrencia import create_ocorrencia, get_ocorrencias_map, get_ocorrencias_list, get_ocorrencia, update_ocorrencia, delete_ocorrencia
from app.cruds.midia import create_midia
from app.cruds.curtida import create_curtida, delete_curtida
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaResponse, Bounds
from app.schemas.curtida import CurtidaCreate, CurtidaResponse
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ocorrencia/", response_model=OcorrenciaResponse)
def create_ocorrencia_route(ocorrencia: OcorrenciaCreate, db: Session = Depends(get_db)):#, midias: Optional[List[UploadFile]] = File(None), ):
    ocorrencia = create_ocorrencia(db, ocorrencia)
    # create_midia(db, midias, ocorrencia.id)
    return ocorrencia 

@router.get("/ocorrencias/map/", response_model=List[OcorrenciaResponse])
def read_ocorrencias_map_route(
    ne_lat: float = Query(...), 
    ne_lng: float = Query(...), 
    sw_lat: float = Query(...), 
    sw_lng: float = Query(...), 
    db: Session = Depends(get_db)):
    return get_ocorrencias_map(db, ne_lat, ne_lng, sw_lat, sw_lng)

@router.get("/ocorrencias/list/", response_model=List[OcorrenciaResponse])
def read_ocorrencias_list_route(
    db: Session = Depends(get_db),
    bairro: Optional[str] = None,
    tipo: Optional[str] = None,
    data_inicio: Optional[str] = Query(None, alias="dataInicio"),
    data_fim: Optional[str] = Query(None, alias="dataFim"),
    limit: int = 10,
    offset: int = 0):
    return get_ocorrencias_list(db, bairro, tipo, data_inicio, data_fim, limit, offset)

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

@router.post("/ocorrencia/{ocorrencia_id}/curtidas/", response_model=CurtidaResponse)
def add_curtida_route(curtida: CurtidaCreate, db: Session = Depends(get_db)):
    curtida = create_curtida(db, curtida)
    
    return curtida

@router.delete("/ocorrencia/{ocorrencia_id}/curtidas/", response_model=CurtidaResponse)
def delete_curtida_route(curtida_id: int, db: Session = Depends(get_db)):
    db_curtida = delete_curtida(db, curtida_id)
    
    if not db_curtida:
        raise HTTPException(status_code=404, detail="Curtida not found")
    
    return db_curtida