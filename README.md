# SOS Backend

Este é o repositório para o backend do projeto SOS defesa civil. Feito com FastAPI, SQLAlchemy, e Alembic.

## Instalação

### 1. Clone o repositório

```
git clone https://github.com/sos-defesa-civil/sos-backend.git

cd sos-backend
```

### 2. Crie e ative o ambiente virtual

Linux/macOS:

```
python3 -m venv venv

source venv/bin/activate
```
Windows:

```
python -m venv venv

venv\Scripts\activate
```

### 3. Instalar dependências


```
pip install -r requirements.txt
```

### 4. Configurando a database

Usando o alembic para criar as migrations e as tabelas da database.

```
alembic upgrade head
```

### 5. Rodando a aplicação

Para iniciar o servidor FastAPI, rode o comando:

```
uvicorn app.main:app --reload
```

O API estará disponível em ``http://127.0.0.1:8000``.

## Database Migrations

Quando fizer alterações nos modelos do SQLAlchemy, crie as novas migrações usando o Alembic:  

```
alembic revision --autogenerate -m "Your migration message"

alembic upgrade head
```
