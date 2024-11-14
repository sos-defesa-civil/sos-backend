from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.repositories.midia import create_midia, get_midia, delete_midia, get_midias_by_oc_id
from app.database import get_db
from app.schemas.midia import MidiaBase, MidiaResponse
from app.models.midia import Midia
from typing import List

import os


router = APIRouter()

@router.post("/midia/", response_model=List[MidiaResponse])
def create_midia_route(midias: List[UploadFile], ocorrencia_id: int, tipo: str, db: Session = Depends(get_db)):
    return create_midia(db, midias, ocorrencia_id, tipo)


@router.get("/midia/{midia_id}", response_model=MidiaResponse)
def read_midia_route(midia_id: int, db: Session = Depends(get_db)):
    db_midia = get_midia(db, midia_id)
    if not db_midia:
        raise HTTPException(status_code=404, detail="Midia not found")
    return db_midia

@router.delete("/midia/{midia_id}", response_model=MidiaResponse)
def delete_midia_route(midia_id: int, db: Session = Depends(get_db)):
    db_midia = delete_midia(db, midia_id)
    if not db_midia:
        raise HTTPException(status_code=404, detail="Midia not found")
    return db_midia

@router.get("/midia/ocorrencia/{oc_id}", response_model=List[MidiaBase])
def get_midias_route(oc_id: int, db: Session = Depends(get_db)):
    midias = get_midias_by_oc_id(db, oc_id)
    if not midias:
        raise HTTPException(status_code=404, detail="Midia not found for this Ocorrencia ID")
    return midias

@router.get("/midia/file/{midia_id}")
def get_midia_file(midia_id: int, db: Session = Depends(get_db)):
    midia = db.query(Midia).filter(Midia.id == midia_id).first()
    if not midia or not os.path.exists(midia.caminho):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(midia.caminho)

