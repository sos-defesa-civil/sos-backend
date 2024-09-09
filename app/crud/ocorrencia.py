from sqlalchemy.orm import Session
from app.models.ocorrencia import Ocorrencia
from typing import List

def create_ocorrencia(db: Session, user_id: int, tipo: str, descricao: str, data_registro: str, ultima_atualizacao: str) -> Ocorrencia:
    db_ocorrencia = Ocorrencia(user_id=user_id, tipo=tipo, descricao=descricao, data_registro=data_registro, ultima_atualizacao=ultima_atualizacao)
    db.add(db_ocorrencia)
    db.commit()
    db.refresh(db_ocorrencia)
    return db_ocorrencia

def get_ocorrencias(db: Session, skip: int = 0, limit: int = 10) -> List[Ocorrencia]:
    return db.query(Ocorrencia).offset(skip).limit(limit).all()

def get_ocorrencia(db: Session, ocorrencia_id: int) -> Ocorrencia:
    return db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()

def update_ocorrencia(db: Session, ocorrencia_id: int, tipo: str, descricao: str, data_registro: str, ultima_atualizacao: str) -> Ocorrencia:
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    if db_ocorrencia:
        db_ocorrencia.tipo = tipo
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
