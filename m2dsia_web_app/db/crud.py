# db/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import User as UserModel
from schemas.schemas import UserCreate, UserUpdate
from typing import List, Optional

def create_user(db: Session, user: UserCreate) -> UserModel:
    """
    Create a new user in the database
    """
    try:
        db_user = UserModel(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"User with email {user.email} already exists")
    except Exception as e:
        db.rollback()
        raise e

def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
    """
    Get a user by ID
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """
    Get a user by email
    """
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
    """
    Get all users with pagination
    """
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_all_users(db: Session) -> List[UserModel]:
    """
    Get all users
    """
    return db.query(UserModel).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[UserModel]:
    """
    Update a user
    """
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user
    """
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e

def get_users_by_class(db: Session, classe: str) -> List[UserModel]:
    """
    Get users by class
    """
    return db.query(UserModel).filter(UserModel.classe == classe).all()

def get_active_users(db: Session) -> List[UserModel]:
    """
    Get only active users
    """
    return db.query(UserModel).filter(UserModel.is_active == True).all()

def deactivate_user(db: Session, user_id: int) -> Optional[UserModel]:
    """
    Deactivate a user instead of deleting
    """
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e