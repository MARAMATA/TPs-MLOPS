# schemas/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    classe: str

class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    classe: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """Schema for returning user data"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # CORRECTION: Utiliser model_config au lieu de class Config
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    """Schema for API responses"""
    id: int
    email: str
    nom: str
    prenom: str
    classe: str
    is_active: bool
    
    # CORRECTION: Utiliser model_config au lieu de class Config
    model_config = ConfigDict(from_attributes=True)