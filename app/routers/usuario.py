from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.usuario import CidadaoCreate, FuncionarioDefesaCivilCreate, UsuarioUpdate, UsuarioResponse, CidadaoResponse, FuncionarioResponse, Login
from app.cruds.usuario import create_cidadao, create_funcionario, get_usuario, get_usuarios, update_usuario, delete_usuario
from app.auth.password import verify_password
from app.auth.token import create_access_token, get_current_user, create_session_data
from app.models.usuario import Usuario
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

@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user

# Get user by ID
@router.get("/usuario/{usuario_id}", response_model=UsuarioResponse)
def read_user(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_usuario

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    # Check if user exists and if password is correct
    if not db_usuario or not verify_password(form_data.password, db_usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a JWT token with the user's email
    access_token = create_access_token(data={"sub": db_usuario.email})
    create_session_data(db, db_usuario.id)
    
    return {"access_token": access_token, "token_type": "bearer"}

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
