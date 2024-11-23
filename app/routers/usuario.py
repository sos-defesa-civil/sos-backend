from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.usuario import CidadaoCreate, FuncionarioCreate, UsuarioUpdate, UsuarioResponse, CidadaoResponse, FuncionarioResponse
from app.repositories.usuario import create_cidadao, create_funcionario, get_usuario, get_usuarios, update_usuario, delete_usuario
from app.auth.password import verify_password
from app.auth.token import create_access_token, get_current_user, create_session_data
from app.models.usuario import Usuario
from app.database import get_db

router = APIRouter()

# Endpoint to create a Cidadao
@router.post(
    "/cidadao/",
    response_model=CidadaoResponse,
    summary="Cadastrar novo usuário do tipo cidadão",
    description=(
        "Esta rota permite cadastrar um novo registro de cidadão no sistema. "
        "Os dados necessários para cadastrar o cidadão devem ser fornecidos no corpo da requisição, "
        "seguindo o esquema definido pelo modelo `CidadaoCreate`."
        "\n\n"
        "### Processos executados:\n"
        "1. Recebe os dados do cidadão fornecidos no corpo da requisição.\n"
        "2. Cria um novo registro no banco de dados.\n"
        "3. Retorna os dados do cidadão recém-criado no formato do modelo `UsuarioResponse`."
    ),
    responses={
        400: {
            "description": "Erro de validação (CPF ou Email já existe)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "CPF already exists"
                    }
                }
            }
        }
    }
)
def create_cidadao_endpoint(cidadao: CidadaoCreate, db: Session = Depends(get_db)):
    return create_cidadao(db, cidadao)


# Endpoint to create a Funcionario_Defesa_Civil
@router.post(
    "/funcionario/",
    response_model=FuncionarioResponse,
    summary="Cadastrar novo usuário do tipo funcionário",
    description=(
        "Esta rota permite cadastrar um novo registro de funcionário da Defesa Civil no sistema. "
        "Os dados necessários para cadastrar o funcionário devem ser fornecidos no corpo da requisição, "
        "seguindo o esquema definido pelo modelo `FuncionarioDefesaCivilCreate`."
        "\n\n"
        "### Processos executados:\n"
        "1. Recebe os dados do funcionário fornecidos no corpo da requisição.\n"
        "2. Cria um novo registro no banco de dados.\n"
        "3. Retorna os dados do funcionário recém-criado no formato do modelo `UsuarioResponse`."
    ),
    responses={
        400: {
            "description": "Erro de validação (CPF ou Email já existe)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "CPF already exists"
                    }
                }
            }
        }
    }
)
def create_funcionario_endpoint(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    return create_funcionario(db, funcionario)
@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Obter informações do usuário autenticado",
    description=(
        "Esta rota retorna as informações do usuário atualmente autenticado no sistema. "
        "É necessário estar autenticado e fornecer um token válido para acessar esta rota."
        "\n\n"
        "### Processos executados:\n"
        "1. Verifica o token de autenticação fornecido.\n"
        "2. Recupera as informações do usuário associado ao token.\n"
        "3. Retorna os dados do usuário no formato do modelo `UsuarioResponse`."
    ),
    responses={
        401: {
            "description": "Erro de autenticação. O token fornecido é inválido ou está ausente.",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            },
        }
    },
)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user

# Get user by ID
@router.get(
    "/usuario/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Obter informações de um usuário",
    description=(
        "Esta rota permite buscar as informações de um usuário específico no sistema. "
        "É necessário fornecer um `usuario_id` válido."
    ),
    responses={
        404: {
            "description": "Usuário não encontrado. O ID fornecido não corresponde a nenhum registro no sistema.",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            },
        }
    },
)
def read_user(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_usuario

@router.post(
    "/login",
    summary="Autenticar usuário",
    description=(
        "Esta rota permite que um usuário faça login no sistema utilizando suas credenciais "
        "(e-mail e senha). Se as credenciais forem válidas, um token JWT será retornado, que "
        "pode ser usado para autenticação em outras rotas protegidas."
        "\n\n"
        "### Processos executados:\n"
        "1. Verifica se o e-mail está registrado no sistema.\n"
        "2. Valida se a senha fornecida está correta.\n"
        "3. Gera um token de acesso JWT para o usuário autenticado.\n"
        "4. Salva os dados de sessão no banco de dados.\n"
        "5. Retorna o token gerado."
    ),
    responses={
        401: {
            "description": "Erro de autenticação. O e-mail ou senha estão incorretos.",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            },
        },
    },
)
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
@router.get(
    "/usuario/",
    response_model=list[UsuarioResponse],
    summary="Obter todos os usuários",
    description=(
        "Esta rota retorna uma lista de todos os usuários no sistema, com suporte a paginação. "
        "É possível controlar a quantidade de resultados e a página através dos parâmetros `skip` e `limit`."
        "\n\n"
    ),
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_usuarios(db, skip=skip, limit=limit)

# Update a user

@router.put("/usuario/{usuario_id}", 
    response_model=UsuarioResponse,
    summary="Atualizar um usuário", 
    description="Atualiza os dados de um usuário existente com base no ID fornecido.",
    responses={
        404: {
            "description": "Usuário não encontrado", 
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Usuário não encontrado"
                    }
                }
            }
        }
    }
)
def update_user(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    return update_usuario(db, usuario_id, usuario)

# Delete a user
@router.delete("/usuario/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Deletar um usuário", 
    description="Deleta os dados de um usuário existente com base no ID fornecido.",
    responses={
        404: {
            "description": "Usuário não encontrado", 
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Usuário não encontrado"
                    }
                }
            }
        }
    }
)
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    return delete_usuario(db, usuario_id)
