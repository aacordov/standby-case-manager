"""
Tests de integración para endpoints de casos.
Prueba creación, lectura, actualización y gestión de casos.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Case, CaseStatus, Priority


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
            "novedades_y_comentarios": "Comentario de prueba",
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
            "novedades_y_comentarios": "Comentario"
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
            "novedades_y_comentarios": "Comentario"
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
            "novedades_y_comentarios": "Comentario"
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
            "novedades_y_comentarios": "Comentario"
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
        assert len(data) == len(multiple_cases)
    
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
        assert len(data) <= 5
    
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
        for case in data:
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
        for case in data:
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
        assert len(data) > 0
        assert any(case["codigo"] == sample_case.codigo for case in data)
    
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
