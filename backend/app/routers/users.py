from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from typing import List

from app.database import get_session
from app.models import User, UserCreate, UserRead, UserRole, UserUpdate
from app.auth import get_current_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


# ============================================================
# ENDPOINT 1: Listar todos los usuarios (GET /)
# ============================================================
@router.get("/", response_model=List[UserRead])
async def read_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Lista todos los usuarios. Solo para administradores."""
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


# ============================================================
# ENDPOINT 2: Obtener UN usuario por ID (GET /{user_id})
# ⭐ NUEVO - Este endpoint faltaba
# ============================================================
@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene un usuario específico por su ID.
    Solo accesible para administradores.
    """
    # Verificar permisos
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Buscar el usuario
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    
    # Si no existe, devolver 404
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user


# ============================================================
# ENDPOINT 3: Crear nuevo usuario (POST /)
# ============================================================
@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Crea un nuevo usuario. Solo para administradores."""
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Verificar si el email ya existe
    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el usuario
    # ⚠️ CAMBIO: user.dict() está deprecado, usar model_dump()
    user_data = user.model_dump(exclude={"password"})
    hashed_pw = get_password_hash(user.password)
    db_user = User(**user_data, hashed_password=hashed_pw)
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


# ============================================================
# ENDPOINT 4: Actualizar usuario (PATCH /{user_id})
# ⭐ MODIFICADO - Agregar manejo de IntegrityError
# ============================================================
@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Actualiza un usuario existente. Solo para administradores."""
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Buscar el usuario
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # ⚠️ CAMBIO: user_update.dict() está deprecado, usar model_dump()
    user_data = user_update.model_dump(exclude_unset=True)
    
    # Si se está actualizando la contraseña, hashearla
    if "password" in user_data and user_data["password"]:
        hashed_pw = get_password_hash(user_data["password"])
        user_data["hashed_password"] = hashed_pw
        del user_data["password"]
    
    # Aplicar cambios
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    
    # ⭐ NUEVO: Manejo de errores de integridad (ej: email duplicado)
    try:
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError as e:
        await session.rollback()
        
        # Verificar si el error es por email duplicado
        error_msg = str(e.orig).lower()
        if "email" in error_msg or "unique" in error_msg:
            raise HTTPException(
                status_code=409,  # 409 Conflict
                detail="Email already exists"
            )
        
        # Otro tipo de error de integridad
        raise HTTPException(
            status_code=400,
            detail="Database integrity error"
        )


# ============================================================
# ENDPOINT 5: Eliminar usuario (DELETE /{user_id})
# ============================================================
@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Elimina un usuario. Solo para administradores."""
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await session.delete(user)
    await session.commit()
    return {"ok": True}