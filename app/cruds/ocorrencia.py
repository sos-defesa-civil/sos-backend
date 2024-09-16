from sqlalchemy.orm import Session
from app.models.ocorrencia import Ocorrencia
from app.schemas.ocorrencia import OcorrenciaCreate
from typing import List, Optional



def create_ocorrencia(db: Session, ocorrencia: OcorrenciaCreate) -> Ocorrencia:
    db_ocorrencia = Ocorrencia(
        user_id=ocorrencia.user_id,
        tipo=ocorrencia.tipo,
        bairro=ocorrencia.bairro,
        descricao=ocorrencia.descricao,
        data_registro=ocorrencia.data_registro,
        ultima_atualizacao=ocorrencia.ultima_atualizacao,
        latitude=ocorrencia.latitude,
        longitude=ocorrencia.longitude
    )
    
    db.add(db_ocorrencia)
    db.commit()
    db.refresh(db_ocorrencia)
    
    return db_ocorrencia

def get_ocorrencias_map(db: Session, ne_lat: float, ne_lng: float, sw_lat: float, sw_lng: float) -> List[Ocorrencia]:
    return db.query(Ocorrencia).filter(
        Ocorrencia.latitude.between(sw_lat, ne_lat),
        Ocorrencia.longitude.between(sw_lng, ne_lng)
    ).all()

def get_ocorrencias_list(
    db: Session, 
    bairro: Optional[str], 
    tipo: Optional[str], 
    data_inicio: Optional[str], 
    data_fim: Optional[str],
    limit: int,
    offset: int
) -> List[Ocorrencia]:
    
    query = db.query(Ocorrencia)
    
    # Add filters conditionally
    if bairro:
        query = query.filter(Ocorrencia.bairro == bairro)
    
    if tipo:
        query = query.filter(Ocorrencia.tipo == tipo)
    
    if data_inicio and data_fim:
        query = query.filter(Ocorrencia.data_registro.between(data_inicio, data_fim))
    elif data_inicio:
        query = query.filter(Ocorrencia.data_registro >= data_inicio)
    elif data_fim:
        query = query.filter(Ocorrencia.data_registro <= data_fim)

    # Apply pagination
    query = query.offset(offset).limit(limit)

    return query.all()

def get_ocorrencia(db: Session, ocorrencia_id: int) -> Ocorrencia:
    return db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()

def update_ocorrencia(db: Session, ocorrencia_id: int, tipo: str, bairro: str, descricao: str, data_registro: str, ultima_atualizacao: str) -> Ocorrencia:
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    if db_ocorrencia:
        db_ocorrencia.tipo = tipo
        db_ocorrencia.bairro = bairro
        db_ocorrencia.descricao = descricao
        db_ocorrencia.data_registro = data_registro
        db_ocorrencia.ultima_atualizacao = ultima_atualizacao
        db.commit()
        db.refresh(db_ocorrencia)
    return db_ocorrencia

def delete_ocorrencia(db: Session, ocorrencia_id: int) -> Ocorrencia:
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    if db_ocorrencia:
        db.delete(db_ocorrencia)
        db.commit()
    return db_ocorrencia
