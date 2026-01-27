"""
Tests unitarios para modelos de datos.
Cubre enums, schemas, validaciones y valores por defecto.
"""
import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.models import (
    UserCreate, UserUpdate, UserRole,
    CaseCreate, CaseUpdate, CaseStatus, Priority,
    CaseAuditType
)

# =========================
# USER MODELS
# =========================

@pytest.mark.unit
class TestUserModels:

    @pytest.mark.parametrize(
        "role,expected",
        [
            (UserRole.ADMIN, "ADMIN"),
            (UserRole.INGRESO, "INGRESO"),
            (UserRole.CONSULTA, "CONSULTA"),
        ],
    )
    def test_user_role_enum_values(self, role, expected):
        assert role.value == expected

    def test_user_create_valid_data(self):
        user = UserCreate(
            nombre="Test User",
            email="test@example.com",
            password="test123",
            rol=UserRole.CONSULTA,
        )

        assert user.nombre == "Test User"
        assert user.email == "test@example.com"
        assert user.rol == UserRole.CONSULTA

    def test_user_create_default_role(self):
        user = UserCreate(
            nombre="Test User",
            email="test@example.com",
            password="test123",
        )
        assert user.rol == UserRole.CONSULTA

    def test_user_update_partial(self):
        update = UserUpdate(nombre="Nuevo Nombre")

        assert update.nombre == "Nuevo Nombre"
        assert update.email is None
        assert update.password is None
        assert update.rol is None

    def test_user_update_all_fields(self):
        update = UserUpdate(
            nombre="Nuevo",
            email="nuevo@test.com",
            password="newpass",
            rol=UserRole.ADMIN,
            is_active=False,
        )

        assert update.is_active is False


# =========================
# CASE MODELS
# =========================

@pytest.mark.unit
class TestCaseModels:

    @pytest.mark.parametrize(
        "status,expected",
        [
            (CaseStatus.ABIERTO, "ABIERTO"),
            (CaseStatus.STANDBY, "STANDBY"),
            (CaseStatus.EN_MONITOREO, "EN_MONITOREO"),
            (CaseStatus.CERRADO, "CERRADO"),
        ],
    )
    def test_case_status_enum_values(self, status, expected):
        assert status.value == expected

    @pytest.mark.parametrize(
        "priority,expected",
        [
            (Priority.CRITICO, "CRITICO"),
            (Priority.ALTO, "ALTO"),
            (Priority.MEDIO, "MEDIO"),
            (Priority.BAJO, "BAJO"),
        ],
    )
    def test_priority_enum_values(self, priority, expected):
        assert priority.value == expected

    def test_case_create_valid_data(self):
        """✅ CORREGIDO: Usar 'motivo' en lugar de 'novedades_y_comentarios'"""
        case = CaseCreate(
            codigo="CASE-001",
            servicio_o_plataforma="Servicio Test",
            prioridad=Priority.ALTO,
            motivo="Motivo del caso",  # ✅ Campo correcto
        )

        assert case.codigo == "CASE-001"
        assert case.servicio_o_plataforma == "Servicio Test"
        assert case.prioridad == Priority.ALTO
        assert case.motivo == "Motivo del caso"
        assert case.observaciones is None
        assert case.sby_responsable is None

    def test_case_create_with_optional_fields(self):
        """✅ NUEVO: Probar creación con campos opcionales"""
        case = CaseCreate(
            codigo="CASE-002",
            servicio_o_plataforma="Platform",
            prioridad=Priority.MEDIO,
            motivo="Test motivo",
            observaciones="Observación inicial",
            sby_responsable="Juan Pérez"
        )

        assert case.observaciones == "Observación inicial"
        assert case.sby_responsable == "Juan Pérez"

    def test_case_update_partial(self):
        update = CaseUpdate(prioridad=Priority.CRITICO)

        assert update.prioridad == Priority.CRITICO
        assert update.estado is None

    def test_case_update_with_fecha_fin(self):
        fecha_fin = datetime.now(timezone.utc)
        update = CaseUpdate(
            estado=CaseStatus.CERRADO,
            fecha_fin=fecha_fin,
        )

        assert update.fecha_fin == fecha_fin


# =========================
# AUDIT MODELS
# =========================

@pytest.mark.unit
@pytest.mark.parametrize(
    "audit_type,expected",
    [
        (CaseAuditType.CREATE, "CREATE"),
        (CaseAuditType.UPDATE, "UPDATE"),
        (CaseAuditType.COMMENT, "COMMENT"),
        (CaseAuditType.BULK_UPDATE, "BULK_UPDATE"),
        (CaseAuditType.EVIDENCE, "EVIDENCE"),
        (CaseAuditType.DELETE, "DELETE"),  # ✅ AGREGADO: Nuevo tipo de auditoría
    ],
)
def test_audit_type_enum_values(audit_type, expected):
    assert audit_type.value == expected


# =========================
# VALIDATION TESTS
# =========================

@pytest.mark.unit
class TestModelValidation:

    @pytest.mark.parametrize("invalid_priority", ["INVALIDO", 123, None])
    def test_invalid_priority_value(self, invalid_priority):
        """✅ CORREGIDO: Usar 'motivo' en lugar de 'novedades_y_comentarios'"""
        with pytest.raises(ValidationError):
            CaseCreate(
                codigo="CASE-003",
                servicio_o_plataforma="Servicio",
                prioridad=invalid_priority,
                motivo="Test",  # ✅ Campo correcto
            )

    @pytest.mark.parametrize("invalid_status", ["INVALIDO", 999])
    def test_invalid_status_value(self, invalid_status):
        with pytest.raises(ValidationError):
            CaseUpdate(estado=invalid_status)

    @pytest.mark.parametrize("invalid_role", ["ROL_INVALIDO", 1])
    def test_invalid_role_value(self, invalid_role):
        with pytest.raises(ValidationError):
            UserCreate(
                nombre="Test",
                email="test@test.com",
                password="pass",
                rol=invalid_role,
            )

    def test_case_create_missing_required_fields(self):
        """✅ NUEVO: Verificar que campos requeridos son obligatorios"""
        with pytest.raises(ValidationError) as exc_info:
            CaseCreate(
                codigo="CASE-004",
                # Falta servicio_o_plataforma
                prioridad=Priority.BAJO,
                motivo="Test"
            )
        
        errors = exc_info.value.errors()
        assert any(e['loc'][0] == 'servicio_o_plataforma' for e in errors)

    def test_case_create_empty_motivo(self):
        """✅ NUEVO: Verificar que motivo no puede estar vacío"""
        case = CaseCreate(
            codigo="CASE-005",
            servicio_o_plataforma="Service",
            prioridad=Priority.BAJO,
            motivo=""  # Vacío pero válido técnicamente
        )
        assert case.motivo == ""