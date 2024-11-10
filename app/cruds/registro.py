from sqlalchemy.orm import Session
from app.models.registro import Registro

def create_log(db: Session, user_id: int, log_type: str, log_description):
    new_log = Registro(
        user_id=user_id,
        tipo=log_type,
        descricao=log_description
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_logs(db: Session):
    query = db.query(Registro)

    return query.all()
