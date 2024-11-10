from sqlalchemy.orm import Session
from app.models.feedback import Feedback  # Assuming you have a Feedback model in `app.models.feedback`
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from app.cruds.registro import create_log
from typing import List, Optional

def create_feedback(db: Session, feedback: FeedbackCreate, user_id: int) -> Feedback:
    db_feedback = Feedback(
        titulo=feedback.titulo,
        descricao=feedback.descricao,
        status=feedback.status,
        data_registro=feedback.data_registro,
        user_id=feedback.user_id,
        oc_id=feedback.oc_id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    # Log the creation action
    description = f"Created Feedback ID: {db_feedback.id}, Title: '{db_feedback.titulo}', Status: '{db_feedback.status}'"
    create_log(db, user_id, "CREATE", description)
    
    return db_feedback

def get_feedback(db: Session, feedback_id: int) -> Optional[Feedback]:
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()

def get_feedback_list(db: Session, oc_id: Optional[int] = None, status: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[FeedbackResponse]:
    query = db.query(Feedback)
    if oc_id:
        query = query.filter(Feedback.oc_id == oc_id)
    if status:
        query = query.filter(Feedback.status == status)
    return query.offset(offset).limit(limit).all()

def update_feedback(db: Session, feedback_id: int, feedback_data: FeedbackUpdate, user_id: int) -> Optional[Feedback]:
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        # Capture the old values for logging
        old_values = {
            "titulo": db_feedback.titulo,
            "descricao": db_feedback.descricao,
            "status": db_feedback.status,
            "data_registro": db_feedback.data_registro
        }

        # Apply updates only to fields that have been provided
        db_feedback.titulo = feedback_data.titulo
        db_feedback.descricao = feedback_data.descricao
        db_feedback.status = feedback_data.status
        db_feedback.data_registro = feedback_data.data_registro
        
        # Commit the update
        db.commit()
        db.refresh(db_feedback)
        
        # Capture the new values and create a description of the changes
        updated_values = {
            "titulo": db_feedback.titulo,
            "descricao": db_feedback.descricao,
            "status": db_feedback.status,
            "data_registro": db_feedback.data_registro
        }
        
        description = (
            f"Updated Feedback ID {feedback_id}. Changes: "
            + ", ".join(
                f"{key}: '{old_values[key]}' -> '{updated_values[key]}'"
                for key in old_values if old_values[key] != updated_values[key]
            )
        )
        
        # Log the update action
        create_log(db, user_id, "UPDATE", description)
    
    return db_feedback

def delete_feedback(db: Session, feedback_id: int, user_id: int) -> Optional[Feedback]:
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        # Log the deletion action before deleting
        description = f"Deleted Feedback ID {db_feedback.id}, Title: '{db_feedback.titulo}', Status: '{db_feedback.status}'"
        create_log(db, user_id, "DELETE", description)
        
        # Delete the feedback
        db.delete(db_feedback)
        db.commit()
    
    return db_feedback
