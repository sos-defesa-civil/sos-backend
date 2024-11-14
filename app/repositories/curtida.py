from sqlalchemy.orm import Session
from app.models.curtida import Curtida
from app.schemas.curtida import CurtidaCreate
from typing import List

def create_curtida(db: Session, curtida: CurtidaCreate) -> Curtida:
    db_curtida = Curtida(user_id=curtida.user_id, oc_id=curtida.oc_id, data_registro=curtida.data_registro)
    
    db.add(db_curtida)
    db.commit()
    db.refresh(db_curtida)
    
    return db_curtida

def delete_curtida(db: Session, curtida_id: int) -> Curtida:
    db_curtida = db.query(Curtida).filter(Curtida.id == curtida_id).first()
    
    if db_curtida:
        db.delete(db_curtida)
        db.commit()
    
    return db_curtida