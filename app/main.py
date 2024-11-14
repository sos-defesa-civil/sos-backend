from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import ocorrencia, usuario, feedback, midia, registro, dashboard

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

Base.metadata.create_all(bind=engine)

app.include_router(ocorrencia.router, prefix="/api", tags=["Ocorrência"])
app.include_router(usuario.router, prefix="/api", tags=["Usuário"])
app.include_router(feedback.router, prefix="/api", tags=["FeedBack"])
app.include_router(midia.router, prefix="/api", tags=["Mídia"])
app.include_router(registro.router, prefix="/api", tags=["Registro"])
app.include_router(dashboard.router, prefix="/api", tags=["DashBoard"])
