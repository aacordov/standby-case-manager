from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON
from pydantic import EmailStr


# ==========================================================
# ENUMS
# ==========================================================

class UserRole(str, Enum):
    CONSULTA = "CONSULTA"
    INGRESO = "INGRESO"
    ADMIN = "ADMIN"


class CaseStatus(str, Enum):
    ABIERTO = "ABIERTO"
    STANDBY = "STANDBY"
    EN_MONITOREO = "EN_MONITOREO"
    CERRADO = "CERRADO"


class Priority(str, Enum):
    CRITICO = "CRITICO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"


class CaseAuditType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    COMMENT = "COMMENT"
    BULK_UPDATE = "BULK_UPDATE"
    EVIDENCE = "EVIDENCE"
    DELETE = "DELETE"


# ==========================================================
# USER
# ==========================================================

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str
    email: str = Field(unique=True, index=True)

    hashed_password: str
    rol: UserRole = Field(default=UserRole.CONSULTA)

    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str
    rol: UserRole = UserRole.CONSULTA


class UserRead(SQLModel):
    id: int
    nombre: str
    email: str
    rol: UserRole
    is_active: bool


class UserUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[UserRole] = None
    is_active: Optional[bool] = None


class PasswordChange(SQLModel):
    current_password: str
    new_password: str


# ==========================================================
# TOKEN
# ==========================================================

class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None


# ==========================================================
# CASE
# ==========================================================

class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    codigo: str = Field(unique=True, index=True)

    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_fin: Optional[datetime] = None

    estado: CaseStatus = Field(default=CaseStatus.ABIERTO)

    sby_responsable: Optional[str] = None
    servicio_o_plataforma: str

    prioridad: Priority = Field(default=Priority.MEDIO)

    motivo: str = Field(default="")
    observaciones: Optional[str] = None

    creado_por_id: Optional[int] = Field(default=None, foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ======================================================
    # RELATIONSHIPS (CRITICAL FIX FOR DELETE CASCADE)
    # ======================================================

    observaciones_list: List["Observation"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"passive_deletes": True}
    )

    attachments: List["Attachment"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"passive_deletes": True}
    )

    audit_logs: List["CaseAudit"] = Relationship(
        sa_relationship_kwargs={"passive_deletes": True}
    )


# ==========================================================
# CASE SCHEMAS
# ==========================================================

class CaseCreate(SQLModel):
    codigo: str
    servicio_o_plataforma: str
    prioridad: Priority
    motivo: str
    observaciones: Optional[str] = None
    sby_responsable: Optional[str] = None


class CaseUpdate(SQLModel):
    codigo: Optional[str] = None
    servicio_o_plataforma: Optional[str] = None
    prioridad: Optional[Priority] = None
    estado: Optional[CaseStatus] = None
    sby_responsable: Optional[str] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    fecha_fin: Optional[datetime] = None


class CaseRead(SQLModel):
    id: int
    codigo: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    estado: CaseStatus
    sby_responsable: Optional[str]
    servicio_o_plataforma: str
    prioridad: Priority
    motivo: str
    observaciones: Optional[str]
    creado_por_id: Optional[int]
    updated_at: datetime
    created_at: datetime


# ==========================================================
# OBSERVATION
# ==========================================================

class Observation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    case_id: int = Field(
        foreign_key="case.id",
        ondelete="CASCADE"
    )

    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
    edited_at: Optional[datetime] = None

    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")

    case: Optional[Case] = Relationship(
        back_populates="observaciones_list"
    )

    created_by: Optional[User] = Relationship()


class ObservationUpdate(SQLModel):
    content: str


# ==========================================================
# ATTACHMENT
# ==========================================================

class Attachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    filename: str
    file_path: str
    file_size: int
    content_type: str

    case_id: int = Field(
        foreign_key="case.id",
        ondelete="CASCADE"
    )

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    case: Optional[Case] = Relationship(
        back_populates="attachments"
    )


class AttachmentRead(SQLModel):
    id: int
    filename: str
    file_path: str
    file_size: int
    content_type: str
    uploaded_at: datetime


# ==========================================================
# CASE AUDIT
# ==========================================================

class CaseAudit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    case_id: int = Field(
        foreign_key="case.id",
        ondelete="CASCADE"
    )

    user_id: int = Field(
        foreign_key="user.id",
        ondelete="CASCADE"
    )

    action: CaseAuditType

    details: Dict = Field(
        default={},
        sa_column=Column(JSON)
    )

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship()


# ==========================================================
# CASE READ WITH DETAILS
# ==========================================================

class CaseReadWithDetails(CaseRead):
    observaciones_list: List[Observation] = []
    attachments: List[AttachmentRead] = []
