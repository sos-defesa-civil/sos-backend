from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import CidadaoCreate, FuncionarioDefesaCivilCreate, UsuarioUpdate, UsuarioResponse, CidadaoResponse, FuncionarioResponse
from app.cruds.usuario import create_cidadao, create_funcionario, get_usuario, get_usuarios, update_usuario, delete_usuario
from app.database import get_db

router = APIRouter()

# Endpoint to create a Cidadao
@router.post("/cidadao/", response_model=UsuarioResponse)
def create_cidadao_endpoint(cidadao: CidadaoCreate, db: Session = Depends(get_db)):
    return create_cidadao(db, cidadao)


# Endpoint to create a Funcionario_Defesa_Civil
@router.post("/funcionario/", response_model=UsuarioResponse)
def create_funcionario_endpoint(funcionario: FuncionarioDefesaCivilCreate, db: Session = Depends(get_db)):
    return create_funcionario(db, funcionario)

# Get user by ID
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def read_user(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_usuario

# Get all users with pagination
@router.get("/", response_model=list[UsuarioResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_usuarios(db, skip=skip, limit=limit)

# Update a user
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_user(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    return update_usuario(db, usuario_id, usuario)

# Delete a user
@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    return delete_usuario(db, usuario_id)
