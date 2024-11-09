from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import ocorrencia, usuario, feedback, midia

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

app.include_router(ocorrencia.router, prefix="/api", tags=["ocorrencia"])
app.include_router(usuario.router, prefix="/api", tags=["usuario"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])
app.include_router(midia.router, prefix="/api", tags=["midia"])

