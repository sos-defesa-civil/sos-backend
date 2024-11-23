from sqlalchemy.orm import Session
from app.models.usuario import Usuario, Cidadao, Funcionario_Defesa_Civil
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, CidadaoCreate, CidadaoResponse, FuncionarioCreate, FuncionarioResponse
from app.auth.password import hash_password
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError



# Create a base user (shared between both Cidadao and Funcionario)
def create_base_usuario(db: Session, usuario_data: UsuarioCreate) -> Usuario:
    db_usuario = Usuario(
        nome=usuario_data.nome,
        data_nascimento=usuario_data.data_nascimento,
        cpf=usuario_data.cpf,
        email=usuario_data.email,
        senha=hash_password(usuario_data.senha),  # You should hash the password here
        admin=usuario_data.admin,
    )
    try:
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction to avoid breaking subsequent operations
        # Check the type of integrity error
        if "cpf" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="CPF already exists")
        elif "email" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=400, detail="An error occurred while creating the user")

    return db_usuario

# Create Cidadao
def create_cidadao(db: Session, cidadao_data: CidadaoCreate) -> CidadaoResponse:
    db_usuario = create_base_usuario(db, cidadao_data)  # Create base user first

    db_cidadao = Cidadao(
        user_id=db_usuario.id,
        endereco=cidadao_data.endereco,
        num_ocorrencias_registradas=cidadao_data.num_ocorrencias_registradas,
        telefone=cidadao_data.telefone,
        celular=cidadao_data.celular
    )
    db.add(db_cidadao)
    db.commit()
    db.refresh(db_cidadao)
    
    cidadao = CidadaoResponse(
        id=db_usuario.id,

        nome=db_usuario.nome,
        data_nascimento=db_usuario.data_nascimento,
        cpf=db_usuario.cpf,
        email=db_usuario.email,  # You should hash the password here
        admin=db_usuario.admin,
        user_id=db_usuario.id,
        endereco=db_cidadao.endereco,
        num_ocorrencias_registradas=db_cidadao.num_ocorrencias_registradas,
        telefone=db_cidadao.telefone,
        celular=db_cidadao.celular
    )
    
    return cidadao

# Create Funcionario_Defesa_Civil
def create_funcionario(db: Session, funcionario_data: FuncionarioCreate) -> FuncionarioResponse:
    db_usuario = create_base_usuario(db, funcionario_data)  # Create base user first
    db_funcionario = Funcionario_Defesa_Civil(
        user_id=db_usuario.id,
        cargo=funcionario_data.cargo,
        nivel_acesso=funcionario_data.nivel_acesso
    )
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    
    funcionario = FuncionarioResponse(
        id=db_usuario.id,
        nome=db_usuario.nome,
        data_nascimento=db_usuario.data_nascimento,
        cpf=db_usuario.cpf,
        email=db_usuario.email,
        admin=db_usuario.admin,
        user_id=db_usuario.id,
        cargo=db_funcionario.cargo,
        nivel_acesso=db_funcionario.nivel_acesso
    )
    return funcionario

# Get user by id
def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

# Get all users
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

# Update user information
def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Delete user
def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_usuario)
    db.commit()
    return db_usuario
