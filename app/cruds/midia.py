from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile
from app.models.midia import Midia
import os
import uuid

def save_file(filename: str, contents: bytes) -> str:
    _, file_extension = os.path.splitext(filename)
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    save_path = os.path.join("./uploads", unique_filename)
    
    with open(save_path, "wb") as f:
        f.write(contents)
    
    return save_path

def create_midia(db: Session, midias: List[UploadFile], ocorrencia_id: int):
    for midia in midias:
        contents = midia.file.read()
        file_path = save_file(midia.filename, contents)

        db_midia = Midia(
            ocorrencia_id=ocorrencia_id,
            file_path=file_path
        )
        db.add(db_midia)

    db.commit()
