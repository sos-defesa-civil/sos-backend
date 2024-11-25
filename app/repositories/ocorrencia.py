from sqlalchemy.orm import Session
from app.models.ocorrencia import Ocorrencia
from app.models.curtida import Curtida
from app.models.midia import Midia
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaResponse, OcorrenciaListResponse, OcorrenciaUpdateResponse
from app.repositories.registro import create_log
from typing import List, Optional
from sqlalchemy import func
import json
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.repositories.feedback import create_feedback
from app.models.usuario import Usuario

def create_ocorrencia(db: Session, ocorrencia: OcorrenciaCreate, user_id) -> OcorrenciaResponse:
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

    # Create initial feedback
    feedback = FeedbackCreate(
        titulo="Ocorrência Criada",
        descricao="Ocorrência criada no sistema",
        status="open",
        data_registro=ocorrencia.data_registro,
        user_id=user_id,
        oc_id=db_ocorrencia.id
    )
    create_feedback(db, feedback, user_id)

    description = f"Criado ocorrencia ID: {db_ocorrencia.id}, {db_ocorrencia}"
    create_log(db, user_id, "CREATE", description)
    
    # Get username for response
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    
    return OcorrenciaResponse(
        id=db_ocorrencia.id,
        user_id=db_ocorrencia.user_id,
        tipo=db_ocorrencia.tipo,
        bairro=db_ocorrencia.bairro,
        descricao=db_ocorrencia.descricao,
        data_registro=db_ocorrencia.data_registro,
        ultima_atualizacao=db_ocorrencia.ultima_atualizacao,
        latitude=db_ocorrencia.latitude,
        longitude=db_ocorrencia.longitude,
        username=usuario.nome,
        curtidas_count=0,
        midias_count=0,
        midias=[],
        feedbacks=[]
    )

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
    type: Optional[int],
    limit: int,
    offset: int
) -> OcorrenciaListResponse:

    # Subquery to get the latest feedback for each occurrence
    latest_feedback = db.query(
        Feedback.oc_id,
        Feedback.status.label('last_status'),
        func.max(Feedback.data_registro).label('max_data')
    ).group_by(
        Feedback.oc_id
    ).subquery()

    # Main query
    base_query = db.query(
        Ocorrencia,
        func.count(Curtida.id).label("curtidas_count"),
        func.count(Midia.id).label("midias_count"),
        Usuario.nome.label("nome"),
        latest_feedback.c.last_status
    ).outerjoin(Ocorrencia.curtidas)\
    .outerjoin(Ocorrencia.midias)\
    .join(Usuario, Ocorrencia.user_id == Usuario.id)\
    .outerjoin(latest_feedback, Ocorrencia.id == latest_feedback.c.oc_id)\
    .group_by(
        Ocorrencia.id, 
        Usuario.nome, 
        latest_feedback.c.last_status,
        Usuario.admin
    ).order_by(Ocorrencia.data_registro.desc())

    if bairro:
        base_query = base_query.filter(Ocorrencia.bairro == bairro)

    if tipo:
        base_query = base_query.filter(Ocorrencia.tipo == tipo)

    if type is not None:
        if type == 0:
            base_query = base_query.filter(Usuario.admin == True)
        elif type == 1:
            base_query = base_query.filter(Usuario.admin == False)

    if data_inicio and data_fim:
        base_query = base_query.filter(Ocorrencia.data_registro.between(data_inicio, data_fim))
    elif data_inicio:
        base_query = base_query.filter(Ocorrencia.data_registro >= data_inicio)
    elif data_fim:
        base_query = base_query.filter(Ocorrencia.data_registro <= data_fim)

    # Get total count before pagination
    total = base_query.count()

    # Apply pagination
    query = base_query.offset(offset).limit(limit)
    ocorrencias = query.all()

    # Convert results to OcorrenciaResponse list
    results = []
    for ocorrencia, curtidas_count, midias_count, nome, last_status in ocorrencias:
        feedbacks = db.query(Feedback).filter(Feedback.oc_id == ocorrencia.id).all()
        feedback_responses = [FeedbackResponse.from_orm(feedback) for feedback in feedbacks]
        results.append(
            OcorrenciaResponse(
                **ocorrencia.__dict__,
                curtidas_count=curtidas_count,
                midias_count=midias_count,
                username=nome,
                status=last_status or "open",
                midias=[],
                feedbacks=feedback_responses
            )
        )

    return {
        "results": results,
        "count": total
    }

def get_ocorrencia(db: Session, ocorrencia_id: int) -> OcorrenciaResponse:
    result = db.query(
        Ocorrencia,
        func.count(Curtida.id).label("curtidas_count"),
        func.count(Midia.id).label("midias_count"),
        Usuario.nome.label("username")
    ).outerjoin(Ocorrencia.curtidas)\
    .outerjoin(Ocorrencia.midias)\
    .join(Usuario, Ocorrencia.user_id == Usuario.id)\
    .filter(Ocorrencia.id == ocorrencia_id)\
    .group_by(Ocorrencia.id, Usuario.nome).first()

    if result:
        ocorrencia, curtidas_count, midias_count, username = result
        midias = db.query(Midia).filter(Midia.oc_id == ocorrencia_id).all()
        feedbacks = db.query(Feedback).filter(Feedback.oc_id == ocorrencia_id).all()
        
        return OcorrenciaResponse(
            **ocorrencia.__dict__,
            username=username,
            curtidas_count=curtidas_count,
            midias_count=midias_count,
            midias=[f"/api/midia/file/{midia.id}" for midia in midias],
            feedbacks=[FeedbackResponse.from_orm(feedback) for feedback in feedbacks]
        )
    return None

def update_ocorrencia(db: Session, ocorrencia_id: int, ocorrencia: Ocorrencia, user_id: int) -> OcorrenciaUpdateResponse:
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
            f"Atualizado ocorrencia ID {ocorrencia_id}. Mudanças: "
            + ", ".join(
                f"{key}: '{old_values[key]}' -> '{updated_values[key]}'"
                for key in old_values if old_values[key] != updated_values[key]
            )
        )
        
        create_log(db, user_id, "UPDATE", description)

    return db_ocorrencia

def delete_ocorrencia(db: Session, ocorrencia_id: int, user_id: int) -> OcorrenciaResponse:
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    if db_ocorrencia:
        # Get the data before deletion for response
        result = db.query(
            Ocorrencia,
            func.count(Curtida.id).label("curtidas_count"),
            func.count(Midia.id).label("midias_count"),
            Usuario.nome.label("username")
        ).outerjoin(Ocorrencia.curtidas)\
        .outerjoin(Ocorrencia.midias)\
        .join(Usuario, Ocorrencia.user_id == Usuario.id)\
        .filter(Ocorrencia.id == ocorrencia_id)\
        .group_by(Ocorrencia.id, Usuario.nome).first()

        ocorrencia, curtidas_count, midias_count, username = result
        midias = db.query(Midia).filter(Midia.oc_id == ocorrencia_id).all()
        feedbacks = db.query(Feedback).filter(Feedback.oc_id == ocorrencia_id).all()

        response = OcorrenciaResponse(
            **ocorrencia.__dict__,
            username=username,
            curtidas_count=curtidas_count,
            midias_count=midias_count,
            midias=[f"/api/midia/file/{midia.id}" for midia in midias],
            feedbacks=[FeedbackResponse.from_orm(feedback) for feedback in feedbacks]
        )

        # Log and delete after creating the response
        description = f"Deletado ocorrencia ID: {db_ocorrencia.id}, {db_ocorrencia}"
        create_log(db, user_id, "DELETE", description)

        db.delete(db_ocorrencia)
        db.commit()

        return response
    return None
