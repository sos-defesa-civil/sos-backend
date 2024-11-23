from datetime import datetime
from app.repositories.curtida import create_curtida, delete_curtida
from app.models.curtida import Curtida
from app.schemas.curtida import CurtidaCreate

def test_create_curtida(db):
    # Configuração do objeto CurtidaCreate com um id fictício
    curtida_data = CurtidaCreate(id=1, user_id=1, oc_id=1, data_registro=datetime.now())
    
    # Chama a função de criação
    curtida = create_curtida(db, curtida=curtida_data)
    
    # Verifica se o retorno não é None e se o id foi criado
    assert curtida is not None
    assert curtida.id is not None
    assert curtida.user_id == curtida_data.user_id
    assert curtida.oc_id == curtida_data.oc_id

def test_delete_curtida(db):
    # Adiciona uma curtida para testar a exclusão
    curtida_data = CurtidaCreate(id=1, user_id=1, oc_id=1, data_registro=datetime.now())
    curtida = create_curtida(db, curtida=curtida_data)
    
    # Chama a função de exclusão
    deleted_curtida = delete_curtida(db, curtida_id=curtida.id)
    
    # Verifica se a curtida foi excluída corretamente
    assert deleted_curtida is not None
    assert deleted_curtida.id == curtida.id
    assert db.query(Curtida).filter(Curtida.id == curtida.id).first() is None
