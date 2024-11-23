from sqlalchemy.orm import Session
from app.models.usuario import Usuario, Cidadao, Funcionario_Defesa_Civil
from typing import List

def get_usuario(db: Session, user_id: int) -> Usuario:
    return db.query(Usuario).filter(Usuario.id == user_id).first()
