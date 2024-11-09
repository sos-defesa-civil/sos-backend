from sqlalchemy.orm import Session
from app.models.feedback import Feedback  # Assuming you have a Feedback model in `app.models.feedback`
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from typing import List, Optional

def create_feedback(db: Session, feedback: FeedbackCreate) -> Feedback:
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

def update_feedback(db: Session, feedback_id: int, feedback_data: FeedbackUpdate) -> Optional[Feedback]:
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        update_data = feedback_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int) -> Optional[Feedback]:
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
    return db_feedback
