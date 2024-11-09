from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackUpdate
from app.cruds.feedback import create_feedback, get_feedback, get_feedback_list, update_feedback, delete_feedback
from app.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/feedback/", response_model=FeedbackResponse)
def create_feedback_route(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    return create_feedback(db, feedback)

@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
def read_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = get_feedback(db, feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback

@router.get("/feedback/", response_model=List[FeedbackResponse])
def read_feedback_list_route(
    oc_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return get_feedback_list(db, oc_id, status, limit, offset)

@router.put("/feedback/{feedback_id}", response_model=FeedbackResponse)
def update_feedback_route(feedback_id: int, feedback: FeedbackUpdate, db: Session = Depends(get_db)):
    db_feedback = update_feedback(db, feedback_id, feedback)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback

@router.delete("/feedback/{feedback_id}", response_model=FeedbackResponse)
def delete_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = delete_feedback(db, feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback
