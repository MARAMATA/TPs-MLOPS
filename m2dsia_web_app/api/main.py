# api/main.py 
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connexion import get_db, engine, get_current_database_info, test_connection
from db.crud import (
    create_user, get_user_by_id, get_user_by_email, get_users, 
    get_all_users, update_user, delete_user, get_users_by_class,
    get_active_users, deactivate_user
)
from schemas.schemas import User, UserCreate, UserUpdate, UserResponse
from models.models import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully")
except Exception as e:
    logger.error(f"❌ Failed to create database tables: {e}")

# Create FastAPI app with enhanced metadata
app = FastAPI(
    title="M2DSIA User Management API",
    description="""
    ## 🎓 M2DSIA User Management API
    
    Une API REST complète pour la gestion des utilisateurs M2DSIA.
    
    ### 🚀 Fonctionnalités
    
    * **Gestion des utilisateurs** : CRUD complet
    * **Recherche avancée** : Par email, classe, statut
    * **Validation automatique** : Pydantic schemas
    * **Base de données** : Support SQLite et AWS RDS MySQL
    * **Documentation** : Swagger UI intégrée
    
    ### 📊 Base de données
    
    Connectée à une base de données avec gestion automatique des migrations.
    
    ### 🔧 Endpoints principaux
    
    * `/users/` - Gestion complète des utilisateurs
    * `/health` - Monitoring de l'API
    * `/info` - Informations système
    """,
    version="2.0.0",
    contact={
        "name": "M2DSIA Team",
        "email": "contact@m2dsia.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Add CORS middleware with enhanced security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# === ENDPOINTS SYSTÈME ===

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return empty favicon to avoid 404 errors"""
    return Response(content="", media_type="image/x-icon")

@app.get("/", tags=["Système"])
async def root():
    """
    🏠 Page d'accueil de l'API
    
    Retourne un message de bienvenue et les informations de base.
    """
    return {
        "message": "Welcome to M2DSIA User Management API",
        "version": "2.0.0",
        "documentation": "/docs",
        "health": "/health",
        "users": "/users/",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Système"])
async def health_check():
    """
    ❤️ Vérification de santé de l'API
    
    Vérifie que l'API et la base de données fonctionnent correctement.
    """
    try:
        # Test database connection
        db_connected = test_connection()
        db_info = get_current_database_info()
        
        return {
            "status": "healthy" if db_connected else "unhealthy",
            "message": "API is running",
            "database": {
                "connected": db_connected,
                "type": db_info.get("type", "Unknown"),
                "host": db_info.get("host", "Local"),
                "database": db_info.get("database", "Unknown")
            },
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/info", tags=["Système"])
async def system_info():
    """
    📊 Informations système
    
    Retourne les informations détaillées sur le système et la base de données.
    """
    try:
        db_info = get_current_database_info()
        
        # Get user statistics
        db = next(get_db())
        total_users = len(get_all_users(db))
        active_users = len(get_active_users(db))
        db.close()
        
        return {
            "api": {
                "name": "M2DSIA User Management API",
                "version": "2.0.0",
                "status": "running"
            },
            "database": db_info,
            "statistics": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users
            },
            "endpoints": {
                "users": "/users/",
                "documentation": "/docs",
                "health": "/health"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to get system info",
                "detail": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

# === ENDPOINTS UTILISATEURS ===

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Utilisateurs"])
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    ➕ Créer un nouveau utilisateur
    
    Crée un nouvel utilisateur avec validation automatique :
    
    * **email** : Adresse email unique (validée)
    * **nom** : Nom de famille
    * **prenom** : Prénom
    * **classe** : Classe ou promotion
    """
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email '{user.email}' already exists"
            )
        
        db_user = create_user(db, user)
        logger.info(f"✅ User created: {user.email}")
        return db_user
    except ValueError as e:
        logger.warning(f"⚠️ Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/", response_model=List[UserResponse], tags=["Utilisateurs"])
async def read_users(
    skip: int = Query(0, ge=0, description="Nombre d'utilisateurs à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'utilisateurs à retourner"),
    db: Session = Depends(get_db)
):
    """
    📋 Lister les utilisateurs avec pagination
    
    Retourne la liste des utilisateurs avec support de la pagination.
    """
    users = get_users(db, skip=skip, limit=limit)
    logger.info(f"📋 Retrieved {len(users)} users (skip={skip}, limit={limit})")
    return users

@app.get("/users/all", response_model=List[UserResponse], tags=["Utilisateurs"])
async def read_all_users(db: Session = Depends(get_db)):
    """
    📋 Lister tous les utilisateurs
    
    Retourne la liste complète de tous les utilisateurs sans pagination.
    """
    users = get_all_users(db)
    logger.info(f"📋 Retrieved all {len(users)} users")
    return users

@app.get("/users/active", response_model=List[UserResponse], tags=["Utilisateurs"])
async def read_active_users(db: Session = Depends(get_db)):
    """
    ✅ Lister les utilisateurs actifs
    
    Retourne uniquement les utilisateurs avec le statut actif.
    """
    users = get_active_users(db)
    logger.info(f"✅ Retrieved {len(users)} active users")
    return users

@app.get("/users/stats", tags=["Utilisateurs"])
async def get_user_statistics(db: Session = Depends(get_db)):
    """
    📊 Statistiques des utilisateurs
    
    Retourne des statistiques détaillées sur les utilisateurs.
    """
    try:
        all_users = get_all_users(db)
        active_users = get_active_users(db)
        
        # Group by class
        classes = {}
        for user in all_users:
            classe = user.classe
            if classe not in classes:
                classes[classe] = {"total": 0, "active": 0}
            classes[classe]["total"] += 1
            if user.is_active:
                classes[classe]["active"] += 1
        
        return {
            "total_users": len(all_users),
            "active_users": len(active_users),
            "inactive_users": len(all_users) - len(active_users),
            "classes": classes,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Utilisateurs"])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    🔍 Obtenir un utilisateur par ID
    
    Retourne les détails d'un utilisateur spécifique par son ID.
    """
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        logger.warning(f"⚠️ User not found: ID {user_id}")
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    logger.info(f"🔍 Retrieved user: {db_user.email}")
    return db_user

@app.get("/users/email/{email}", response_model=UserResponse, tags=["Utilisateurs"])
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    📧 Obtenir un utilisateur par email
    
    Retourne les détails d'un utilisateur spécifique par son adresse email.
    """
    db_user = get_user_by_email(db, email)
    if db_user is None:
        logger.warning(f"⚠️ User not found: {email}")
        raise HTTPException(status_code=404, detail=f"User with email '{email}' not found")
    
    logger.info(f"📧 Retrieved user: {email}")
    return db_user

@app.get("/users/class/{classe}", response_model=List[UserResponse], tags=["Utilisateurs"])
async def read_users_by_class(classe: str, db: Session = Depends(get_db)):
    """
    🎓 Obtenir les utilisateurs par classe
    
    Retourne tous les utilisateurs d'une classe spécifique.
    """
    users = get_users_by_class(db, classe)
    logger.info(f"🎓 Retrieved {len(users)} users from class: {classe}")
    return users

@app.put("/users/{user_id}", response_model=UserResponse, tags=["Utilisateurs"])
async def update_user_endpoint(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    ✏️ Mettre à jour un utilisateur
    
    Met à jour les informations d'un utilisateur existant.
    Seuls les champs fournis seront modifiés.
    """
    db_user = update_user(db, user_id, user_update)
    if db_user is None:
        logger.warning(f"⚠️ User not found for update: ID {user_id}")
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    logger.info(f"✏️ Updated user: {db_user.email}")
    return db_user

@app.delete("/users/{user_id}", tags=["Utilisateurs"])
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    🗑️ Supprimer un utilisateur
    
    Supprime définitivement un utilisateur de la base de données.
    """
    # Get user info before deletion for logging
    user_to_delete = get_user_by_id(db, user_id)
    if user_to_delete is None:
        logger.warning(f"⚠️ User not found for deletion: ID {user_id}")
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Failed to delete user with ID {user_id}")
    
    logger.info(f"🗑️ Deleted user: {user_to_delete.email}")
    return {
        "message": f"User '{user_to_delete.email}' deleted successfully",
        "deleted_user": {
            "id": user_id,
            "email": user_to_delete.email,
            "nom": user_to_delete.nom,
            "prenom": user_to_delete.prenom
        },
        "timestamp": datetime.now().isoformat()
    }

@app.patch("/users/{user_id}/deactivate", response_model=UserResponse, tags=["Utilisateurs"])
async def deactivate_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    🔒 Désactiver un utilisateur
    
    Désactive un utilisateur sans le supprimer (soft delete).
    L'utilisateur peut être réactivé plus tard.
    """
    db_user = deactivate_user(db, user_id)
    if db_user is None:
        logger.warning(f"⚠️ User not found for deactivation: ID {user_id}")
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    logger.info(f"🔒 Deactivated user: {db_user.email}")
    return db_user

@app.patch("/users/{user_id}/activate", response_model=UserResponse, tags=["Utilisateurs"])
async def activate_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    🔓 Réactiver un utilisateur
    
    Réactive un utilisateur précédemment désactivé.
    """
    try:
        user_update = UserUpdate(is_active=True)
        db_user = update_user(db, user_id, user_update)
        if db_user is None:
            logger.warning(f"⚠️ User not found for activation: ID {user_id}")
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        logger.info(f"🔓 Activated user: {db_user.email}")
        return db_user
    except Exception as e:
        logger.error(f"❌ Error activating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === ENDPOINTS DE RECHERCHE ===

@app.get("/search/users", response_model=List[UserResponse], tags=["Recherche"])
async def search_users(
    q: Optional[str] = Query(None, description="Terme de recherche (nom, prénom, email)"),
    classe: Optional[str] = Query(None, description="Filtrer par classe"),
    active: Optional[bool] = Query(None, description="Filtrer par statut actif"),
    db: Session = Depends(get_db)
):
    """
    🔍 Recherche avancée d'utilisateurs
    
    Recherche des utilisateurs avec différents critères :
    
    * **q** : Recherche dans nom, prénom et email
    * **classe** : Filtrer par classe
    * **active** : Filtrer par statut (actif/inactif)
    """
    try:
        users = get_all_users(db)
        
        # Filter by search query
        if q:
            q_lower = q.lower()
            users = [
                user for user in users
                if q_lower in user.nom.lower() 
                or q_lower in user.prenom.lower() 
                or q_lower in user.email.lower()
            ]
        
        # Filter by class
        if classe:
            users = [user for user in users if user.classe == classe]
        
        # Filter by active status
        if active is not None:
            users = [user for user in users if user.is_active == active]
        
        logger.info(f"🔍 Search query='{q}', classe='{classe}', active={active} - Found {len(users)} users")
        return users
        
    except Exception as e:
        logger.error(f"❌ Error in search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === GESTION DES ERREURS ===

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Gestionnaire d'erreur 404 personnalisé"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "timestamp": datetime.now().isoformat(),
            "documentation": "/docs"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Gestionnaire d'erreur 500 personnalisé"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An internal server error occurred",
            "timestamp": datetime.now().isoformat(),
            "support": "contact@m2dsia.com"
        }
    )

# === ÉVÉNEMENTS D'APPLICATION ===

@app.on_event("startup")
async def startup_event():
    """Événements au démarrage de l'application"""
    logger.info("🚀 M2DSIA API is starting up...")
    
    # Test database connection
    if test_connection():
        db_info = get_current_database_info()
        logger.info(f"✅ Database connected: {db_info}")
    else:
        logger.error("❌ Database connection failed")
    
    logger.info("🎉 M2DSIA API started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Événements à l'arrêt de l'application"""
    logger.info("🛑 M2DSIA API is shutting down...")
    logger.info("👋 Goodbye!")

# === POINT D'ENTRÉE ===

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting M2DSIA User Management API...")
    logger.info("📊 Version: 2.0.0")
    logger.info("🌐 Documentation: http://localhost:8000/docs")
    logger.info("❤️ Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=False,  # Set to True in development
        access_log=True
    )