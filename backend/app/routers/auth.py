from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.database import get_session
from app.models import User, UserCreate, UserRead, Token, UserRole, PasswordChange
from app.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ============================================================
# ENDPOINT 1: Registrar nuevo usuario (POST /register)
# ============================================================
@router.post("/register", response_model=UserRead)
async def register(
    user: UserCreate, 
    session: AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    """
    Registra un nuevo usuario en el sistema.
    Solo los administradores pueden registrar usuarios.
    """
    # Verificar permisos
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, 
            detail="Only admins can register users"
        )
    
    # Verificar si el email ya existe
    statement = select(User).where(User.email == user.email)
    result = await session.execute(statement)
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    # Crear el usuario
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        nombre=user.nombre, 
        email=user.email, 
        hashed_password=hashed_pw, 
        rol=user.rol
    )
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


# ============================================================
# ENDPOINT 2: Login (POST /login)
# ⭐ MODIFICADO - Validar usuario activo
# ============================================================
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(get_session)
):
    """
    Autentica un usuario y devuelve un token de acceso.
    Verifica credenciales y que el usuario esté activo.
    """
    # Buscar usuario por email
    statement = select(User).where(User.email == form_data.username)
    result = await session.execute(statement)
    user = result.scalars().first()
    
    # Verificar credenciales
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ⭐ NUEVO: Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }


# ============================================================
# ENDPOINT 3: Obtener usuario actual (GET /me)
# ============================================================
@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve la información del usuario autenticado actualmente.
    """
    return current_user


# ============================================================
# ENDPOINT 4: Cambiar contraseña (POST /change-password)
# ============================================================
@router.post("/change-password")
async def change_password(
    password_change: PasswordChange,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Permite al usuario autenticado cambiar su propia contraseña.
    Requiere la contraseña actual para validar la identidad.
    """
    # Verificar que la contraseña actual sea correcta
    if not verify_password(
        password_change.current_password, 
        current_user.hashed_password
    ):
        raise HTTPException(
            status_code=400, 
            detail="Incorrect current password"
        )
    
    # Actualizar con la nueva contraseña hasheada
    current_user.hashed_password = get_password_hash(password_change.new_password)
    session.add(current_user)
    await session.commit()
    
    return {"message": "Password updated successfully"}