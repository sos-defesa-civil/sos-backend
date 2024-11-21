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

@router.post(
    "/midia/",
    response_model=List[MidiaResponse],
    summary="Upload de mídias relacionadas a uma ocorrência",
    description=(
        "Esta rota permite o upload de arquivos de mídia associados a uma ocorrência específica. "
        "É possível enviar múltiplos arquivos em uma única requisição.\n\n"
        "### Processos executados:\n"
        "1. Verifica se a ocorrência especificada existe no banco de dados.\n"
        "2. Salva as mídias no banco de dados e armazena os arquivos.\n"
        "3. Retorna os dados das mídias criadas."
    ),
)
def create_midia_route(midias: List[UploadFile], ocorrencia_id: int, tipo: str, db: Session = Depends(get_db)):
    return create_midia(db, midias, ocorrencia_id, tipo)


@router.get(
    "/midia/{midia_id}",
    response_model=MidiaResponse,
    summary="Obter informações de uma mídia",
    description=(
        "Esta rota permite buscar as informações de uma mídia específica a partir de seu ID. "
        "Se a mídia existir no banco de dados, seus detalhes serão retornados.\n\n"
        "### Processos executados:\n"
        "1. Verifica se o ID da mídia existe no banco de dados.\n"
        "2. Retorna os detalhes da mídia."
    ),
    responses={
        404: {
            "description": "Mídia não encontrada.",
            "content": {
                "application/json": {
                    "example": {"detail": "Midia not found"}
                }
            },
        },
    },
)
def read_midia_route(midia_id: int, db: Session = Depends(get_db)):
    db_midia = get_midia(db, midia_id)
    if not db_midia:
        raise HTTPException(status_code=404, detail="Midia not found")
    return db_midia

@router.delete(
    "/midia/{midia_id}",
    response_model=MidiaResponse,
    summary="Deletar uma mídia",
    description=(
        "Esta rota permite deletar uma mídia específica a partir do seu ID. "
        "Se a mídia existir, ela será removida do banco de dados e os detalhes da mídia deletada serão retornados.\n\n"
        "### Processos executados:\n"
        "1. Verifica se o ID da mídia existe no banco de dados.\n"
        "2. Remove o registro da mídia do banco de dados.\n"
        "3. Deleta o arquivo armazenado.\n"
        "4. Retorna os detalhes da mídia deletada."
    ),
    responses={
        404: {
            "description": "Mídia não encontrada.",
            "content": {
                "application/json": {
                    "example": {"detail": "Midia not found"}
                }
            },
        },
    },
)
def delete_midia_route(midia_id: int, db: Session = Depends(get_db)):
    db_midia = delete_midia(db, midia_id)
    if not db_midia:
        raise HTTPException(status_code=404, detail="Midia not found")
    return db_midia

@router.get(
    "/midia/ocorrencia/{oc_id}",
    response_model=List[MidiaBase],
    summary="Listar mídias de uma ocorrência",
    description=(
        "Esta rota permite obter a lista de mídias associadas a uma ocorrência específica com base no seu ID.\n\n"
        "### Processos executados:\n"
        "1. Verifica se existem mídias vinculadas ao ID da ocorrência fornecido.\n"
        "2. Retorna a lista de mídias relacionadas."
    )
)
def get_midias_route(oc_id: int, db: Session = Depends(get_db)):
    midias = get_midias_by_oc_id(db, oc_id)
    if not midias:
        raise HTTPException(status_code=404, detail="Midia not found for this Ocorrencia ID")
    return midias

@router.get(
    "/midia/file/{midia_id}",
    summary="Baixar arquivo de mídia",
    description=(
        "Esta rota permite o download do arquivo de mídia associado a um ID específico.\n\n"
        "### Processos executados:\n"
        "1. Verifica se a mídia com o ID fornecido existe no banco de dados.\n"
        "2. Confirma se o arquivo físico associado ao caminho armazenado existe no sistema.\n"
        "3. Retorna o arquivo como resposta para download."
    ),
    responses={
        404: {
            "description": "Mídia ou arquivo físico não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "File not found"}
                }
            },
        },
    },
)
def get_midia_file(
    midia_id: int,
    db: Session = Depends(get_db),
):
    midia = db.query(Midia).filter(Midia.id == midia_id).first()
    if not midia or not os.path.exists(midia.caminho):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(midia.caminho)
def get_midia_file(midia_id: int, db: Session = Depends(get_db)):
    midia = db.query(Midia).filter(Midia.id == midia_id).first()
    if not midia or not os.path.exists(midia.caminho):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(midia.caminho)

