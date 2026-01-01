import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlmodel import SQLModel

from app.main import app
from app.database import get_session
from app.models import User, UserRole
from app.auth import get_password_hash, create_access_token


# ------------------------------------------------------------------
# CONFIGURACIÓN DB TEST
# ------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# ------------------------------------------------------------------
# EVENT LOOP (pytest-asyncio)
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ------------------------------------------------------------------
# CREAR / DESTRUIR TABLAS (UNA SOLA VEZ)
# ------------------------------------------------------------------

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# ------------------------------------------------------------------
# SESIÓN DB CON LIMPIEZA ENTRE TESTS
# ------------------------------------------------------------------

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        # Rollback para limpiar cualquier transacción pendiente
        await session.rollback()


# ------------------------------------------------------------------
# LIMPIEZA DE DATOS ENTRE TESTS
# ------------------------------------------------------------------

@pytest_asyncio.fixture(autouse=True)
async def clean_database():
    """Limpia todas las tablas antes de cada test para evitar conflictos."""
    yield  # El test se ejecuta aquí
    
    # Después del test, limpiar todas las tablas
    # Nota: "case" es palabra reservada en SQL, por eso usamos comillas dobles
    async with engine.begin() as conn:
        from sqlalchemy import text
        await conn.execute(text('DELETE FROM caseaudit'))
        await conn.execute(text('DELETE FROM attachment'))
        await conn.execute(text('DELETE FROM observation'))
        await conn.execute(text('DELETE FROM "case"'))  # Escapado porque "case" es palabra reservada
        await conn.execute(text('DELETE FROM user'))


# ------------------------------------------------------------------
# OVERRIDE DEPENDENCY FASTAPI
# ------------------------------------------------------------------

@pytest_asyncio.fixture(autouse=True)
async def override_get_db(db_session: AsyncSession):
    async def _override():
        yield db_session

    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()


# ------------------------------------------------------------------
# CLIENT HTTP ASYNC
# ------------------------------------------------------------------

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ------------------------------------------------------------------
# FIXTURES DE USUARIOS
# ------------------------------------------------------------------

@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    """Crea un usuario administrador para testing."""
    user = User(
        nombre="Admin User",
        email="admin@test.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        rol=UserRole.ADMIN,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def ingreso_user(db_session: AsyncSession) -> User:
    """Crea un usuario con rol INGRESO para testing."""
    user = User(
        nombre="Ingreso User",
        email="ingreso@test.com",
        hashed_password=get_password_hash("ingreso123"),
        is_active=True,
        rol=UserRole.INGRESO,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


# ------------------------------------------------------------------
# FIXTURES DE AUTENTICACIÓN (HEADERS CON TOKENS)
# ------------------------------------------------------------------

@pytest_asyncio.fixture
async def admin_token(admin_user: User) -> str:
    """Genera un token JWT para el usuario administrador."""
    access_token = create_access_token(data={"sub": admin_user.email})
    return access_token


@pytest_asyncio.fixture
async def ingreso_token(ingreso_user: User) -> str:
    """Genera un token JWT para el usuario de ingreso."""
    access_token = create_access_token(data={"sub": ingreso_user.email})
    return access_token


@pytest_asyncio.fixture
async def admin_headers(admin_token: str) -> dict:
    """Headers de autenticación para requests como administrador."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest_asyncio.fixture
async def ingreso_headers(ingreso_token: str) -> dict:
    """Headers de autenticación para requests como usuario de ingreso."""
    return {"Authorization": f"Bearer {ingreso_token}"}


@pytest_asyncio.fixture
async def consulta_user(db_session: AsyncSession) -> User:
    """Crea un usuario con rol CONSULTA para testing."""
    user = User(
        nombre="Consulta User",
        email="consulta@test.com",
        hashed_password=get_password_hash("consulta123"),
        is_active=True,
        rol=UserRole.CONSULTA,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def consulta_token(consulta_user: User) -> str:
    """Genera un token JWT para el usuario de consulta."""
    access_token = create_access_token(data={"sub": consulta_user.email})
    return access_token


@pytest_asyncio.fixture
async def consulta_headers(consulta_token: str) -> dict:
    """Headers de autenticación para requests como usuario de consulta."""
    return {"Authorization": f"Bearer {consulta_token}"}


@pytest_asyncio.fixture
async def inactive_user(db_session: AsyncSession) -> User:
    """Crea un usuario inactivo para testing."""
    user = User(
        nombre="Inactive User",
        email="inactive@test.com",
        hashed_password=get_password_hash("inactive123"),
        is_active=False,
        rol=UserRole.CONSULTA,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


# ------------------------------------------------------------------
# FIXTURES DE CASOS
# ------------------------------------------------------------------

@pytest_asyncio.fixture
async def sample_case(db_session: AsyncSession, admin_user: User):
    """Crea un caso de ejemplo para testing."""
    from app.models import Case, CaseStatus, Priority
    
    case = Case(
        codigo="SAMPLE-001",
        servicio_o_plataforma="Plataforma de Prueba",
        prioridad=Priority.MEDIO,
        novedades_y_comentarios="Caso de prueba",
        observaciones="Observación inicial",
        sby_responsable="Responsable Test",
        estado=CaseStatus.ABIERTO,
        creado_por_id=admin_user.id,
    )
    db_session.add(case)
    await db_session.commit()
    await db_session.refresh(case)
    return case


@pytest_asyncio.fixture
async def multiple_cases(db_session: AsyncSession, admin_user: User):
    """Crea múltiples casos para testing."""
    from app.models import Case, CaseStatus, Priority
    
    cases = []
    priorities = [Priority.CRITICO, Priority.ALTO, Priority.MEDIO, Priority.BAJO]
    statuses = [CaseStatus.ABIERTO, CaseStatus.STANDBY, CaseStatus.EN_MONITOREO]
    
    for i in range(10):
        case = Case(
            codigo=f"MULTI-{i+1:03d}",
            servicio_o_plataforma=f"Servicio {i+1}",
            prioridad=priorities[i % len(priorities)],
            novedades_y_comentarios=f"Comentario del caso {i+1}",
            estado=statuses[i % len(statuses)],
            sby_responsable=f"Responsable {i+1}",
            creado_por_id=admin_user.id,
        )
        db_session.add(case)
        cases.append(case)
    
    await db_session.commit()
    
    # Refresh all cases
    for case in cases:
        await db_session.refresh(case)
    
    return cases


@pytest_asyncio.fixture
async def case_with_observations(db_session: AsyncSession, admin_user: User):
    """Crea un caso con observaciones para testing."""
    from app.models import Case, CaseStatus, Priority, Observation
    
    # Crear el caso
    case = Case(
        codigo="CASE-WITH-OBS",
        servicio_o_plataforma="Servicio con Observaciones",
        prioridad=Priority.ALTO,
        novedades_y_comentarios="Caso con múltiples observaciones",
        estado=CaseStatus.ABIERTO,
        creado_por_id=admin_user.id,
    )
    db_session.add(case)
    await db_session.commit()
    await db_session.refresh(case)
    
    # Crear observaciones
    observations = []
    for i in range(3):
        obs = Observation(
            case_id=case.id,
            content=f"Observación {i+1} del caso",
            created_by_id=admin_user.id,
        )
        db_session.add(obs)
        observations.append(obs)
    
    await db_session.commit()
    
    # Refresh case to load relationships
    await db_session.refresh(case)
    
    return case