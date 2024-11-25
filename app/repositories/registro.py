from sqlalchemy.orm import Session
from app.models.registro import Registro
from app.models.usuario import Usuario

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
    query = db.query(
        Registro,
        Usuario.nome.label('nome')
    ).join(Usuario, Registro.user_id == Usuario.id).order_by(Registro.data.desc())

    results = query.all()
    
    logs = []
    for registro, nome in results:
        log_dict = {
            "id": registro.id,
            "user_id": registro.user_id,
            "username": nome,
            "data": registro.data,
            "tipo": registro.tipo,
            "descricao": registro.descricao
        }
        logs.append(log_dict)
    
    return logs
