from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from app.models.usuario import Usuario
from app.models.usuario import Cidadao
from app.models.usuario import Funcionario_Defesa_Civil
from app.models.ocorrencia import Ocorrencia
from app.models.curtida import Curtida
from app.models.feedback import Feedback
from app.models.midia import Midia
