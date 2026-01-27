"""
Tests de integración para endpoints de casos.
Prueba creación, lectura, actualización y gestión de casos.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models import User, Case, CaseStatus, Priority, Observation, CaseAudit, CaseAuditType

@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestCaseCreation:
    """Tests para creación de casos."""
    
    async def test_create_case_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que un admin puede crear un caso."""
        case_data = {
            "codigo": "TEST-001",
            "servicio_o_plataforma": "Plataforma Test",
            "prioridad": "ALTO",
            "motivo": "Comentario de prueba",
            "observaciones": "Observación inicial",
            "sby_responsable": "Juan Pérez"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == "TEST-001"
        assert data["servicio_o_plataforma"] == "Plataforma Test"
        assert data["prioridad"] == "ALTO"
        assert data["estado"] == "ABIERTO"  # Default status
    
    async def test_create_case_as_ingreso(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict
    ):
        """Verifica que un usuario INGRESO puede crear un caso."""
        case_data = {
            "codigo": "TEST-002",
            "servicio_o_plataforma": "Servicio 2",
            "prioridad": "MEDIO",
            "motivo": "Comentario"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data,
            headers=ingreso_headers
        )
        
        assert response.status_code == 200
    
    async def test_create_case_as_consulta_forbidden(
        self, 
        client: AsyncClient, 
        consulta_headers: dict
    ):
        """Verifica que un usuario CONSULTA no puede crear casos."""
        case_data = {
            "codigo": "TEST-003",
            "servicio_o_plataforma": "Servicio 3",
            "prioridad": "BAJO",
            "motivo": "Comentario"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data,
            headers=consulta_headers
        )
        
        assert response.status_code == 403
        assert "Not authorized to create cases" in response.json()["detail"]
    
    async def test_create_case_duplicate_code(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica que no se puede crear un caso con código duplicado."""
        case_data = {
            "codigo": sample_case.codigo,  # Código ya existe
            "servicio_o_plataforma": "Servicio",
            "prioridad": "BAJO",
            "motivo": "Comentario"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data,
            headers=admin_headers
        )
        
        assert response.status_code == 400
        assert "Case code already exists" in response.json()["detail"]
    
    async def test_create_case_without_auth(self, client: AsyncClient):
        """Verifica que no se puede crear caso sin autenticación."""
        case_data = {
            "codigo": "TEST-004",
            "servicio_o_plataforma": "Servicio",
            "prioridad": "BAJO",
            "motivo": "Comentario"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data
        )
        
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestCaseRetrieval:
    """Tests para obtención de casos."""
    
    async def test_get_all_cases(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica que se pueden obtener todos los casos."""
        response = await client.get(
            "/cases/",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == len(multiple_cases)
    
    async def test_get_cases_with_pagination(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica paginación de casos."""
        response = await client.get(
            "/cases/?skip=0&limit=5",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) <= 5
    
    async def test_get_cases_filter_by_status(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica filtrado de casos por estado."""
        response = await client.get(
            "/cases/?status=ABIERTO",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        for case in data["items"]:
            assert case["estado"] == "ABIERTO"
    
    async def test_get_cases_filter_by_priority(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica filtrado de casos por prioridad."""
        response = await client.get(
            "/cases/?priority=CRITICO",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        for case in data["items"]:
            assert case["prioridad"] == "CRITICO"
    
    async def test_get_cases_search_by_code(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica búsqueda de casos por código."""
        response = await client.get(
            f"/cases/?search={sample_case.codigo}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0
        assert any(case["codigo"] == sample_case.codigo for case in data["items"])
    
    async def test_get_single_case(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica obtención de un caso individual."""
        response = await client.get(
            f"/cases/{sample_case.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == sample_case.codigo
        assert data["id"] == sample_case.id
    
    async def test_get_nonexistent_case(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que devuelve 404 para caso inexistente."""
        response = await client.get(
            "/cases/99999",
            headers=admin_headers
        )
        
        assert response.status_code == 404
        assert "Case not found" in response.json()["detail"]
    
    async def test_get_case_with_observations(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        case_with_observations: Case
    ):
        """Verifica que se obtienen las observaciones del caso."""
        response = await client.get(
            f"/cases/{case_with_observations.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "observaciones_list" in data
        assert len(data["observaciones_list"]) > 0


@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestCaseUpdate:
    """Tests para actualización de casos."""
    
    async def test_update_case_status_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica que un admin puede actualizar el estado de un caso."""
        update_data = {"estado": "CERRADO"}
        
        response = await client.patch(
            f"/cases/{sample_case.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "CERRADO"
    
    async def test_update_case_priority(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica actualización de prioridad de caso."""
        update_data = {"prioridad": "CRITICO"}
        
        response = await client.patch(
            f"/cases/{sample_case.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["prioridad"] == "CRITICO"
    
    async def test_update_case_multiple_fields(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica actualización de múltiples campos."""
        update_data = {
            "estado": "EN_MONITOREO",
            "prioridad": "ALTO",
            "sby_responsable": "Nuevo Responsable"
        }
        
        response = await client.patch(
            f"/cases/{sample_case.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["estado"] == "EN_MONITOREO"
        assert data["prioridad"] == "ALTO"
        assert data["sby_responsable"] == "Nuevo Responsable"
    
    async def test_update_case_as_consulta_forbidden(
        self, 
        client: AsyncClient, 
        consulta_headers: dict,
        sample_case: Case
    ):
        """Verifica que usuario CONSULTA no puede actualizar casos."""
        update_data = {"estado": "CERRADO"}
        
        response = await client.patch(
            f"/cases/{sample_case.id}",
            json=update_data,
            headers=consulta_headers
        )
        
        assert response.status_code == 403
        assert "Not authorized to edit cases" in response.json()["detail"]
    
    async def test_update_nonexistent_case(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que devuelve 404 al actualizar caso inexistente."""
        update_data = {"estado": "CERRADO"}
        
        response = await client.patch(
            "/cases/99999",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestBulkUpdate:
    """Tests para actualización masiva de casos."""
    
    async def test_bulk_close_cases(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica cierre masivo de casos."""
        case_ids = [case.id for case in multiple_cases[:3]]
        bulk_data = {
            "ids": case_ids,
            "action": "CLOSE",
            "value": "CERRADO"
        }
        
        response = await client.post(
            "/cases/bulk-update",
            json=bulk_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert "Updated" in response.json()["message"]
    
    async def test_bulk_assign_cases(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica asignación masiva de responsable."""
        case_ids = [case.id for case in multiple_cases[:2]]
        bulk_data = {
            "ids": case_ids,
            "action": "ASSIGN",
            "value": "Responsable Masivo"
        }
        
        response = await client.post(
            "/cases/bulk-update",
            json=bulk_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
    
    async def test_bulk_update_priority(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica actualización masiva de prioridad."""
        case_ids = [case.id for case in multiple_cases[:2]]
        bulk_data = {
            "ids": case_ids,
            "action": "PRIORITY",
            "value": "CRITICO"
        }
        
        response = await client.post(
            "/cases/bulk-update",
            json=bulk_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
    
    async def test_bulk_update_as_consulta_forbidden(
        self, 
        client: AsyncClient, 
        consulta_headers: dict,
        multiple_cases: list[Case]
    ):
        """Verifica que CONSULTA no puede hacer actualizaciones masivas."""
        case_ids = [case.id for case in multiple_cases[:2]]
        bulk_data = {
            "ids": case_ids,
            "action": "CLOSE",
            "value": "CERRADO"
        }
        
        response = await client.post(
            "/cases/bulk-update",
            json=bulk_data,
            headers=consulta_headers
        )
        
        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestCaseTimeline:
    """Tests para timeline de casos."""
    
    async def test_get_case_timeline(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        case_with_observations: Case
    ):
        """Verifica obtención de timeline de un caso."""
        response = await client.get(
            f"/cases/{case_with_observations.id}/timeline",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verificar que contiene observaciones
        obs_items = [item for item in data if item["type"] == "OBSERVATION"]
        assert len(obs_items) > 0
    
    async def test_timeline_empty_for_new_case(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica que un caso nuevo tiene timeline vacío o mínimo."""
        response = await client.get(
            f"/cases/{sample_case.id}/timeline",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

class TestCaseDelete:
    """Tests para eliminación de casos."""
    
    async def test_delete_case_as_admin_success(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica que un admin puede eliminar casos exitosamente."""
        case_id = sample_case.id
        case_codigo = sample_case.codigo
        
        response = await client.delete(
            f"/cases/{case_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "eliminado exitosamente" in data["message"]
        assert data["deleted_case"]["id"] == case_id
        assert data["deleted_case"]["codigo"] == case_codigo
        
        # Verificar que el caso ya no existe
        get_response = await client.get(
            f"/cases/{case_id}",
            headers=admin_headers
        )
        assert get_response.status_code == 404
    
    async def test_delete_case_as_ingreso_forbidden(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict,
        sample_case: Case
    ):
        """Verifica que usuario INGRESO no puede eliminar casos."""
        response = await client.delete(
            f"/cases/{sample_case.id}",
            headers=ingreso_headers
        )
        
        assert response.status_code == 403
        assert "administradores" in response.json()["detail"].lower()
    
    async def test_delete_case_as_consulta_forbidden(
        self, 
        client: AsyncClient, 
        consulta_headers: dict,
        sample_case: Case
    ):
        """Verifica que usuario CONSULTA no puede eliminar casos."""
        response = await client.delete(
            f"/cases/{sample_case.id}",
            headers=consulta_headers
        )
        
        assert response.status_code == 403
        assert "administradores" in response.json()["detail"].lower()
    
    async def test_delete_nonexistent_case(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que devuelve 404 al eliminar caso inexistente."""
        response = await client.delete(
            "/cases/99999",
            headers=admin_headers
        )
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"].lower()
    
    async def test_delete_case_without_auth(
        self, 
        client: AsyncClient,
        sample_case: Case
    ):
        """Verifica que no se puede eliminar sin autenticación."""
        response = await client.delete(f"/cases/{sample_case.id}")
        
        assert response.status_code == 401
    
    async def test_delete_case_cascade_observations(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        case_with_observations: Case,
        db_session: AsyncSession
    ):
        """Verifica que eliminar caso elimina sus observaciones (CASCADE)."""
        case_id = case_with_observations.id
        
        # Verificar que el caso tiene observaciones
        obs_query = select(Observation).where(Observation.case_id == case_id)
        obs_result = await db_session.execute(obs_query)
        observations_before = obs_result.scalars().all()
        assert len(observations_before) > 0
        
        # Eliminar el caso
        response = await client.delete(
            f"/cases/{case_id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        
        # Verificar que las observaciones se eliminaron
        obs_result_after = await db_session.execute(obs_query)
        observations_after = obs_result_after.scalars().all()
        assert len(observations_after) == 0
    
    async def test_delete_case_cascade_audits(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case,
        db_session: AsyncSession
    ):
        """Verifica que eliminar caso elimina sus registros de auditoría (CASCADE)."""
        case_id = sample_case.id
        
        # Crear una auditoría
        audit = CaseAudit(
            case_id=case_id,
            user_id=1,
            action=CaseAuditType.UPDATE,
            details={"test": "data"}
        )
        db_session.add(audit)
        await db_session.commit()
        
        # Verificar que existe la auditoría
        audit_query = select(CaseAudit).where(CaseAudit.case_id == case_id)
        audit_result = await db_session.execute(audit_query)
        audits_before = audit_result.scalars().all()
        assert len(audits_before) > 0
        
        # Eliminar el caso
        response = await client.delete(
            f"/cases/{case_id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        
        # Verificar que las auditorías se eliminaron
        audit_result_after = await db_session.execute(audit_query)
        audits_after = audit_result_after.scalars().all()
        assert len(audits_after) == 0


# ==========================================================
# PRUEBAS PARA EDICIÓN DE OBSERVACIONES
# ==========================================================

@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestObservationUpdate:
    """Tests para edición de observaciones."""
    
    async def test_update_own_observation_success(
        self, 
        client: AsyncClient, 
        consulta_headers: dict,
        consulta_user,
        db_session: AsyncSession
    ):
        """Verifica que un usuario puede editar su propia observación."""
        # Crear caso
        case = Case(
            codigo="TEST-OBS-001",
            servicio_o_plataforma="Test Service",
            prioridad="MEDIO",
            motivo="Test",
            creado_por_id=consulta_user.id
        )
        db_session.add(case)
        await db_session.commit()
        await db_session.refresh(case)
        
        # Crear observación del usuario CONSULTA
        obs = Observation(
            case_id=case.id,
            content="Contenido original",
            created_by_id=consulta_user.id
        )
        db_session.add(obs)
        await db_session.commit()
        await db_session.refresh(obs)
        
        # Actualizar observación propia
        update_data = {"content": "Contenido actualizado"}
        response = await client.patch(
            f"/cases/observations/{obs.id}",
            json=update_data,
            headers=consulta_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Contenido actualizado"
        assert data["edited_at"] is not None
    
    async def test_update_others_observation_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        consulta_user,
        db_session: AsyncSession
    ):
        """Verifica que un admin puede editar observaciones de otros."""
        # Crear caso y observación de otro usuario
        case = Case(
            codigo="TEST-OBS-002",
            servicio_o_plataforma="Test Service",
            prioridad="MEDIO",
            motivo="Test",
            creado_por_id=consulta_user.id
        )
        db_session.add(case)
        await db_session.commit()
        await db_session.refresh(case)
        
        obs = Observation(
            case_id=case.id,
            content="Observación de CONSULTA",
            created_by_id=consulta_user.id
        )
        db_session.add(obs)
        await db_session.commit()
        await db_session.refresh(obs)
        
        # Admin edita la observación
        update_data = {"content": "Editado por admin"}
        response = await client.patch(
            f"/cases/observations/{obs.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Editado por admin"
    
    async def test_update_others_observation_as_ingreso(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict,
        consulta_user,
        db_session: AsyncSession
    ):
        """Verifica que un usuario INGRESO puede editar observaciones de otros."""
        case = Case(
            codigo="TEST-OBS-003",
            servicio_o_plataforma="Test Service",
            prioridad="MEDIO",
            motivo="Test",
            creado_por_id=consulta_user.id
        )
        db_session.add(case)
        await db_session.commit()
        await db_session.refresh(case)
        
        obs = Observation(
            case_id=case.id,
            content="Observación de CONSULTA",
            created_by_id=consulta_user.id
        )
        db_session.add(obs)
        await db_session.commit()
        await db_session.refresh(obs)
        
        # INGRESO edita la observación
        update_data = {"content": "Editado por INGRESO"}
        response = await client.patch(
            f"/cases/observations/{obs.id}",
            json=update_data,
            headers=ingreso_headers
        )
        
        assert response.status_code == 200
    
    async def test_update_others_observation_forbidden(
        self, 
        client: AsyncClient, 
        consulta_headers: dict,
        admin_user,
        db_session: AsyncSession
    ):
        """Verifica que CONSULTA no puede editar observación ajena."""
        # Crear caso y observación del admin
        case = Case(
            codigo="TEST-OBS-004",
            servicio_o_plataforma="Test Service",
            prioridad="MEDIO",
            motivo="Test",
            creado_por_id=admin_user.id
        )
        db_session.add(case)
        await db_session.commit()
        await db_session.refresh(case)
        
        obs = Observation(
            case_id=case.id,
            content="Observación del admin",
            created_by_id=admin_user.id
        )
        db_session.add(obs)
        await db_session.commit()
        await db_session.refresh(obs)
        
        # Usuario CONSULTA intenta editar
        update_data = {"content": "Intento de edición"}
        response = await client.patch(
            f"/cases/observations/{obs.id}",
            json=update_data,
            headers=consulta_headers
        )
        
        assert response.status_code == 403
        assert "Not authorized" in response.json()["detail"]
    
    async def test_update_nonexistent_observation(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que devuelve 404 al editar observación inexistente."""
        update_data = {"content": "Test"}
        response = await client.patch(
            "/cases/observations/99999",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_update_observation_without_auth(
        self, 
        client: AsyncClient,
        db_session: AsyncSession
    ):
        """Verifica que no se puede editar sin autenticación."""
        # Crear observación
        case = Case(
            codigo="TEST-OBS-005",
            servicio_o_plataforma="Test",
            prioridad="MEDIO",
            motivo="Test"
        )
        db_session.add(case)
        await db_session.commit()
        await db_session.refresh(case)
        
        obs = Observation(
            case_id=case.id,
            content="Test",
            created_by_id=1
        )
        db_session.add(obs)
        await db_session.commit()
        await db_session.refresh(obs)
        
        update_data = {"content": "Test"}
        response = await client.patch(
            f"/cases/observations/{obs.id}",
            json=update_data
        )
        
        assert response.status_code == 401


# ==========================================================
# PRUEBAS PARA SISTEMA DE AUDITORÍA
# ==========================================================

@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestAuditSystem:
    """Tests para sistema de auditoría."""
    
    async def test_audit_created_on_case_update(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case,
        db_session: AsyncSession
    ):
        """Verifica que se crea auditoría al actualizar caso."""
        case_id = sample_case.id
        
        # Actualizar caso
        update_data = {
            "estado": "CERRADO",
            "prioridad": "CRITICO"
        }
        response = await client.patch(
            f"/cases/{case_id}",
            json=update_data,
            headers=admin_headers
        )
        assert response.status_code == 200
        
        # Verificar que se creó auditoría
        audit_query = select(CaseAudit).where(
            CaseAudit.case_id == case_id,
            CaseAudit.action == CaseAuditType.UPDATE
        )
        result = await db_session.execute(audit_query)
        audits = result.scalars().all()
        
        assert len(audits) > 0
        audit = audits[-1]  # Última auditoría
        assert "estado" in audit.details
        assert "prioridad" in audit.details
    
    async def test_audit_details_structure(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case,
        db_session: AsyncSession
    ):
        """Verifica estructura de detalles en auditoría."""
        # Actualizar caso
        update_data = {"sby_responsable": "Nuevo Responsable"}
        await client.patch(
            f"/cases/{sample_case.id}",
            json=update_data,
            headers=admin_headers
        )
        
        # Obtener auditoría
        audit_query = select(CaseAudit).where(
            CaseAudit.case_id == sample_case.id,
            CaseAudit.action == CaseAuditType.UPDATE
        )
        result = await db_session.execute(audit_query)
        audit = result.scalars().first()
        
        assert audit is not None
        assert "sby_responsable" in audit.details
        assert "old" in audit.details["sby_responsable"]
        assert "new" in audit.details["sby_responsable"]
        assert audit.details["sby_responsable"]["new"] == "Nuevo Responsable"
    
    async def test_audit_created_on_bulk_update(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        multiple_cases: list[Case],
        db_session: AsyncSession
    ):
        """Verifica que se crea auditoría en bulk update."""
        case_ids = [case.id for case in multiple_cases[:2]]
        
        # Bulk update
        bulk_data = {
            "ids": case_ids,
            "action": "CLOSE",
            "value": "CERRADO"
        }
        response = await client.post(
            "/cases/bulk-update",
            json=bulk_data,
            headers=admin_headers
        )
        assert response.status_code == 200
        
        # Verificar auditorías
        for case_id in case_ids:
            audit_query = select(CaseAudit).where(
                CaseAudit.case_id == case_id,
                CaseAudit.action == CaseAuditType.BULK_UPDATE
            )
            result = await db_session.execute(audit_query)
            audits = result.scalars().all()
            assert len(audits) > 0
    
    async def test_audit_appears_in_timeline(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case
    ):
        """Verifica que auditorías aparecen en timeline."""
        # Actualizar caso para crear auditoría
        update_data = {"estado": "EN_MONITOREO"}
        await client.patch(
            f"/cases/{sample_case.id}",
            json=update_data,
            headers=admin_headers
        )
        
        # Obtener timeline
        response = await client.get(
            f"/cases/{sample_case.id}/timeline",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        timeline = response.json()
        
        # Verificar que hay eventos de tipo AUDIT
        audit_events = [e for e in timeline if e["type"] == "AUDIT"]
        assert len(audit_events) > 0


# ==========================================================
# PRUEBAS PARA NUEVA ESTRUCTURA DE OBSERVACIONES
# ==========================================================

@pytest.mark.integration
@pytest.mark.cases
@pytest.mark.asyncio
class TestObservationStructure:
    """Tests para nueva estructura de observaciones."""
    
    async def test_create_case_with_initial_observation(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        db_session: AsyncSession
    ):
        """Verifica que observación inicial se guarda como entidad separada."""
        case_data = {
            "codigo": "TEST-NEWOBS-001",
            "servicio_o_plataforma": "Test Service",
            "prioridad": "MEDIO",
            "motivo": "Motivo de prueba",
            "observaciones": "Observación inicial importante"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        case_id = response.json()["id"]
        
        # Verificar que se creó la observación
        obs_query = select(Observation).where(Observation.case_id == case_id)
        result = await db_session.execute(obs_query)
        observations = result.scalars().all()
        
        assert len(observations) == 1
        assert observations[0].content == "Observación inicial importante"
    
    async def test_create_case_without_initial_observation(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        db_session: AsyncSession
    ):
        """Verifica que se puede crear caso sin observación inicial."""
        case_data = {
            "codigo": "TEST-NEWOBS-002",
            "servicio_o_plataforma": "Test Service",
            "prioridad": "BAJO",
            "motivo": "Test sin observación"
        }
        
        response = await client.post(
            "/cases/",
            json=case_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        case_id = response.json()["id"]
        
        # Verificar que no hay observaciones
        obs_query = select(Observation).where(Observation.case_id == case_id)
        result = await db_session.execute(obs_query)
        observations = result.scalars().all()
        
        assert len(observations) == 0
    
    async def test_case_with_multiple_observations(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        sample_case: Case,
        db_session: AsyncSession
    ):
        """Verifica manejo de múltiples observaciones en un caso."""
        case_id = sample_case.id
        
        # Agregar varias observaciones mediante updates
        for i in range(3):
            update_data = {"observaciones": f"Observación número {i+1}"}
            await client.patch(
                f"/cases/{case_id}",
                json=update_data,
                headers=admin_headers
            )
        
        # Obtener caso con observaciones
        response = await client.get(
            f"/cases/{case_id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "observaciones_list" in data
        assert len(data["observaciones_list"]) >= 3