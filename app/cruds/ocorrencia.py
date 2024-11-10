from sqlalchemy.orm import Session
from app.models.ocorrencia import Ocorrencia
from app.models.curtida import Curtida
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaResponse
from app.cruds.registro import create_log
from typing import List, Optional
from sqlalchemy import func
import json

def create_ocorrencia(db: Session, ocorrencia: OcorrenciaCreate, user_id) -> Ocorrencia:
    db_ocorrencia = Ocorrencia(
        user_id=user_id,
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

    description = f"Created Ocorrencia ID: {db_ocorrencia.id}, {db_ocorrencia}"

    create_log(db, user_id, "CREATE", description)
    
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
) -> List[OcorrenciaResponse]:
    
    # Consulta base com join para contar as curtidas
    query = db.query(
        Ocorrencia,
        func.count(Curtida.id).label("curtidas_count")
    ).outerjoin(Ocorrencia.curtidas).group_by(Ocorrencia.id)
    
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

    query = query.offset(offset).limit(limit)

    ocorrencias = query.all()

    # Converta os resultados para uma lista de OcorrenciaResponse
    result = [
        OcorrenciaResponse(
            **ocorrencia.__dict__,
            curtidas_count=curtidas_count
        )
        for ocorrencia, curtidas_count in ocorrencias
    ]

    return result

def get_ocorrencia(db: Session, ocorrencia_id: int) -> Ocorrencia:
    return db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()

def update_ocorrencia(db: Session, ocorrencia_id: int, ocorrencia: Ocorrencia, user_id: int) -> Ocorrencia:
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    
    if db_ocorrencia:
        # Capture the old values for logging
        old_values = {
            "tipo": db_ocorrencia.tipo,
            "bairro": db_ocorrencia.bairro,
            "descricao": db_ocorrencia.descricao,
            "data_registro": db_ocorrencia.data_registro,
            "ultima_atualizacao": db_ocorrencia.ultima_atualizacao,
        }
        
        # Update the fields
        db_ocorrencia.tipo = ocorrencia.tipo
        db_ocorrencia.bairro = ocorrencia.bairro
        db_ocorrencia.descricao = ocorrencia.descricao
        db_ocorrencia.data_registro = ocorrencia.data_registro
        db_ocorrencia.ultima_atualizacao = ocorrencia.ultima_atualizacao

        # Save the update
        db.commit()
        db.refresh(db_ocorrencia)

        # Log the update
        updated_values = {
            "tipo": db_ocorrencia.tipo,
            "bairro": db_ocorrencia.bairro,
            "descricao": db_ocorrencia.descricao,
            "data_registro": db_ocorrencia.data_registro,
            "ultima_atualizacao": db_ocorrencia.ultima_atualizacao,
        }
        
        # Format the log description with the changes
        description = (
            f"Updated Ocorrencia ID {ocorrencia_id}. Changes: "
            + ", ".join(
                f"{key}: '{old_values[key]}' -> '{updated_values[key]}'"
                for key in old_values if old_values[key] != updated_values[key]
            )
        )
        
        create_log(db, user_id, "UPDATE", description)

    return db_ocorrencia

def delete_ocorrencia(db: Session, ocorrencia_id: int, user_id: int) -> Ocorrencia:
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    if db_ocorrencia:

        description = f"Deleted Ocorrencia ID: {db_ocorrencia.id}, {db_ocorrencia}"
        create_log(db, user_id, "DELETE", description)

        db.delete(db_ocorrencia)
        db.commit()
        
    return db_ocorrencia
