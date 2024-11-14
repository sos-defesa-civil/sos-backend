import jwt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.database import get_db
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.usuario import Usuario
from app.models.session_data import SessionData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(weeks=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    
def create_session_data(db: Session, user_id: int):
    # Store refresh token in database with user_id for session tracking
    session = SessionData(user_id=user_id)
    db.add(session)
    db.commit()
    return session

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception