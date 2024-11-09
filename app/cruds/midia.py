from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile
from app.models.midia import Midia

import os
import uuid

def get_midias_by_oc_id(db: Session, oc_id: int) -> List[Midia]:
    return db.query(Midia).filter(Midia.oc_id == oc_id).all()

def save_file(filename: str, contents: bytes) -> str:

    upload_dir = "./midias"

    os.makedirs(upload_dir, exist_ok=True)
    
    _, file_extension = os.path.splitext(filename)
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    save_path = os.path.join(upload_dir, unique_filename)
    
    with open(save_path, "wb") as f:
        f.write(contents)
    
    return save_path

def create_midia(db: Session, midias: List[UploadFile], ocorrencia_id: int, tipo: str):
    midiasResponse = []
    for midia in midias:
        contents = midia.file.read()
        file_path = save_file(midia.filename, contents)

        db_midia = Midia(
            tipo = tipo,
            caminho = file_path,
            oc_id = ocorrencia_id
        )
        db.add(db_midia)

        midiasResponse.append(db_midia)

    db.commit()

    return midiasResponse

def get_midia(db: Session, midia_id: int) -> Midia:
    return db.query(Midia).filter(Midia.id == midia_id).first()

def delete_midia(db: Session, midia_id: int) -> Midia:
    db_midia = db.query(Midia).filter(Midia.id == midia_id).first()
    if db_midia:
        db.delete(db_midia)
        db.commit()
    return db_midia