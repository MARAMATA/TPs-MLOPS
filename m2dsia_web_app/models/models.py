# models/models.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from db.connexion import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255), nullable=False)
    classe = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', nom='{self.nom}', prenom='{self.prenom}')>"