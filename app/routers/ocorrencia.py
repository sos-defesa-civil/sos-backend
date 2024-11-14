from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.repositories.ocorrencia import create_ocorrencia, get_ocorrencias_map, get_ocorrencias_list, get_ocorrencia, update_ocorrencia, delete_ocorrencia
from app.repositories.curtida import create_curtida, delete_curtida
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaResponse, OcorrenciaListResponse
from app.schemas.curtida import CurtidaCreate, CurtidaResponse
from app.auth.token import get_current_user
from app.models.usuario import Usuario
from typing import List, Optional
from app.database import get_db
from datetime import datetime
from app.repositories.feedback import create_feedback
from app.schemas.feedback import FeedbackCreate

router = APIRouter()

@router.post("/ocorrencia/", 
response_model=OcorrenciaResponse, 
summary="Criar Ocorrência", 
description="Cria uma nova ocorrência e associa ao usuário autenticado.")
@router.post("/ocorrencia/", response_model=OcorrenciaResponse)
def create_ocorrencia_route(ocorrencia: OcorrenciaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    ocorrencia = create_ocorrencia(db, ocorrencia, current_user.id)  
    return ocorrencia 

@router.get("/ocorrencias/map/", 
    response_model=List[OcorrenciaResponse],
    summary="Listar Ocorrências no Mapa",
    description="Retorna ocorrências dentro de uma área delimitada pelo mapa. "
                "Os parâmetros `ne_lat`, `ne_lng`, `sw_lat` e `sw_lng` definem os limites,"
                "permitindo que a busca seja limitada a uma região específica.",)

def read_ocorrencias_map_route(
    ne_lat: float = Query(...), 
    ne_lng: float = Query(...), 
    sw_lat: float = Query(...), 
    sw_lng: float = Query(...), 
    db: Session = Depends(get_db)):
    return get_ocorrencias_map(db, ne_lat, ne_lng, sw_lat, sw_lng)

@router.get("/ocorrencias/list/", 
    response_model=OcorrenciaListResponse,
    summary="Listar Ocorrências",
    description="""Retorna uma lista paginada de ocorrências com filtros opcionais. 
                Os parâmetros `bairro` e `tipo` permitem filtrar as ocorrências pelo bairro e tipo de ocorrência, 
                enquanto `dataInicio` e `dataFim` delimitam o intervalo de tempo (formato YYYY-MM-DD). 
                Os parâmetro `limit` e `offset`, permitem o controle a da paginação,
                um define o limite por pagina e o outro a ocorrência inicial, respectivamente
                <br/><br/>
                Tipos Aceitos:
                <ul>
                <li>alagamentos</li>
                <li>colapso_barragens</li>
                <li>colapso_edificios</li>
                <li>colapso_solo</li>
                <li>deslizamentos</li>
                <li>enxurradas</li>
                <li>erosao_costeira</li>
                <li>erosao_margem_fluvial</li>
                <li>inundacoes</li>
                <li>liberacao_quimicos</li>
                <li>tempestade_raios</li>
                <li>tombamentos_rolamentos</li>
                <li>tremor_terra</li>
                </ul>""")
def read_ocorrencias_list_route(
    db: Session = Depends(get_db),
    bairro: Optional[str] = None,
    tipo: Optional[str] = None,
    data_inicio: Optional[str] = Query(None, alias="dataInicio"),
    data_fim: Optional[str] = Query(None, alias="dataFim"),
    limit: int = 10,
    offset: int = 0):

    
    return get_ocorrencias_list(db, bairro, tipo, data_inicio, data_fim, limit, offset)

@router.get("/ocorrencia/{ocorrencia_id}", 
    response_model=OcorrenciaResponse,
    summary="Obter Ocorrência",
    description="Obtém os detalhes de uma ocorrência específica pelo ID.")
def read_ocorrencia_route(ocorrencia_id: int, db: Session = Depends(get_db)):
    db_ocorrencia = get_ocorrencia(db, ocorrencia_id)
    if db_ocorrencia is None:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return db_ocorrencia

@router.put("/ocorrencia/{ocorrencia_id}", 
    response_model=OcorrenciaResponse,
    summary="Atualizar Ocorrência",
    description="Atualiza os detalhes de uma ocorrência específica pelo ID.")
def update_ocorrencia_route(ocorrencia_id: int, ocorrencia: OcorrenciaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_ocorrencia = update_ocorrencia(db, ocorrencia_id, ocorrencia, current_user.id)
    if db_ocorrencia is None:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return db_ocorrencia

@router.delete("/ocorrencia/{ocorrencia_id}", 
    response_model=OcorrenciaResponse,
    summary="Excluir Ocorrência",
    description="Remove uma ocorrência específica pelo ID.")
def delete_ocorrencia_route(ocorrencia_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_ocorrencia = delete_ocorrencia(db, ocorrencia_id, current_user.id)
    if db_ocorrencia is None:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return db_ocorrencia

@router.post("/ocorrencia/{ocorrencia_id}/curtidas/", 
    response_model=CurtidaResponse,
    summary="Adicionar Curtida em Ocorrência",
    description="Adiciona uma curtida a uma ocorrência específica.")
def add_curtida_route(curtida: CurtidaCreate, db: Session = Depends(get_db)):
    curtida = create_curtida(db, curtida)
    
    return curtida
