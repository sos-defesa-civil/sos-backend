from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class SessionData(Base):
    __tablename__ = 'session_data'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Assuming a user model exists
    session_start = Column(DateTime, default=datetime.utcnow)