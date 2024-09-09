from fastapi import FastAPI
from app.database import engine, Base
from app.routers import ocorrencia
from app.models.usuario import Usuario
from app.models.ocorrencia import Ocorrencia

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ocorrencia.router, prefix="/api", tags=["ocorrencia"])

