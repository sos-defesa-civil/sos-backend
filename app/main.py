from fastapi import FastAPI
from app.database import engine, Base
from app.routers import ocorrencia, usuario, feedback, midia

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ocorrencia.router, prefix="/api", tags=["ocorrencia"])
app.include_router(usuario.router, prefix="/api", tags=["usuario"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])
app.include_router(midia.router, prefix="/api", tags=["midia"])

