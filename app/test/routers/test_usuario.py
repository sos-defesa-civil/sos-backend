import pytest
from datetime import datetime
from app.models.usuario import Usuario, Cidadao, Funcionario_Defesa_Civil
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, CidadaoCreate, FuncionarioDefesaCivilCreate
from app.cruds.usuario import (
    create_cidadao, create_funcionario, get_usuario, get_usuarios, 
    update_usuario, delete_usuario, create_base_usuario
)
from app.auth.password import verify_password

# Teste para criar um usuário base
def test_create_base_usuario(db):
    usuario_data = UsuarioCreate(
        nome="João Silva",
        data_nascimento=datetime(1990, 5, 15),
        cpf="12345678900",
        email="joao@example.com",
        senha="senha_segura",
        admin=False
    )
    usuario = create_base_usuario(db, usuario_data)

    assert usuario.id is not None
    assert usuario.nome == "João Silva"
    assert usuario.cpf == "12345678900"
    assert usuario.email == "joao@example.com"
    assert usuario.senha != "senha_segura"  # Senha deve estar hasheada

# Teste para criar um Cidadão
def test_create_cidadao(db):
    cidadao_data = CidadaoCreate(
        nome="Ana Souza",
        data_nascimento=datetime(1985, 3, 20),
        cpf="98765432100",
        email="ana@example.com",
        senha="senha_cidadao",
        admin=False,
        endereco="Rua Principal, 123",
        num_ocorrencias_registradas=5,
        telefone="(11) 2345-6789",
        celular="(11) 91234-5678"
    )
    cidadao = create_cidadao(db, cidadao_data)

    assert cidadao.id is not None
    assert cidadao.cidadao.endereco == "Rua Principal, 123"
    assert cidadao.cidadao.num_ocorrencias_registradas == 5

# Teste para criar um Funcionário de Defesa Civil
def test_create_funcionario(db):
    funcionario_data = FuncionarioDefesaCivilCreate(
        nome="Carlos Pereira",
        data_nascimento=datetime(1970, 8, 10),
        cpf="11122233344",
        email="carlos@example.com",
        senha="senha_funcionario",
        admin=True,
        cargo="Coordenador",
        nivel_acesso="Alto"
    )
    funcionario = create_funcionario(db, funcionario_data)

    assert funcionario.id is not None
    assert funcionario.funcionario.cargo == "Coordenador"
    assert funcionario.funcionario.nivel_acesso == "Alto"

# Teste para obter um usuário por ID
def test_get_usuario(db):
    usuario = get_usuario(db, 1)
    assert usuario is not None
    assert usuario.id == 1

# Teste para obter todos os usuários
def test_get_usuarios(db):
    usuarios = get_usuarios(db)
    assert len(usuarios) > 0  # Verifica que há pelo menos um usuário

# Teste para atualizar um usuário
def test_update_usuario(db):
    update_data = UsuarioUpdate(
        nome="João Silva Atualizado",
        data_nascimento=datetime(1990, 5, 15),
        cpf="12345678900",
        email="joao_atualizado@example.com",
        senha="nova_senha_segura",
        admin=True
    )
    usuario = update_usuario(db, 1, update_data)

    assert usuario.nome == "João Silva Atualizado"
    assert usuario.email == "joao_atualizado@example.com"
    assert usuario.admin == True

# Teste para deletar um usuário
def test_delete_usuario(db):
    usuario = delete_usuario(db, 1)
    assert usuario is not None
    assert usuario.id == 1
    assert get_usuario(db, 1) is None  # Verifica se o usuário foi realmente deletado

# Teste de login (verifica se a senha está hasheada e corresponde ao login)
def test_login(db):
    senha = "senha_segura"
    usuario_data = UsuarioCreate(
        nome="Login Teste",
        data_nascimento=datetime(1990, 5, 15),
        cpf="12312312300",
        email="login@example.com",
        senha=senha,
        admin=False
    )
    usuario = create_base_usuario(db, usuario_data)
    
    assert verify_password(senha, usuario.senha)  # Verifica se a senha bate com o hash
