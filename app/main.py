from fastapi import FastAPI
from app.database import engine, Base
from app.routers import ocorrencia
from app.routers import usuario

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ocorrencia.router, prefix="/api", tags=["ocorrencia"])
app.include_router(usuario.router, prefix="/api", tags=["usuario"])

