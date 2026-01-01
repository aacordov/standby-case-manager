"""
Tests de integración para endpoints de gestión de usuarios.
Prueba listado, actualización y desactivación de usuarios.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserRole


@pytest.mark.integration
@pytest.mark.users
@pytest.mark.asyncio
class TestUserManagement:
    """Tests para gestión de usuarios."""
    
    async def test_list_users_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        admin_user: User,
        ingreso_user: User,
        consulta_user: User
    ):
        """Verifica que un admin puede listar usuarios."""
        response = await client.get(
            "/users/",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3  # Al menos los 3 usuarios de fixtures
        
        # Verificar que contiene los usuarios creados
        emails = [user["email"] for user in data]
        assert admin_user.email in emails
        assert ingreso_user.email in emails
        assert consulta_user.email in emails
    
    async def test_list_users_as_non_admin_forbidden(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict
    ):
        """Verifica que no-admin no puede listar usuarios."""
        response = await client.get(
            "/users/",
            headers=ingreso_headers
        )
        
        # Dependiendo de la implementación, puede ser 403 o no tener el endpoint
        # Asumiendo que solo admin puede acceder
        assert response.status_code in [403, 404]
    
    async def test_get_user_by_id_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        ingreso_user: User
    ):
        """Verifica que admin puede obtener un usuario por ID."""
        response = await client.get(
            f"/users/{ingreso_user.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ingreso_user.id
        assert data["email"] == ingreso_user.email
        assert data["rol"] == UserRole.INGRESO.value
    
    async def test_update_user_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        ingreso_user: User
    ):
        """Verifica que admin puede actualizar un usuario."""
        update_data = {
            "nombre": "Nombre Actualizado",
            "rol": "ADMIN"
        }
        
        response = await client.patch(
            f"/users/{ingreso_user.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Nombre Actualizado"
        assert data["rol"] == "ADMIN"
    
    async def test_deactivate_user_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        ingreso_user: User
    ):
        """Verifica que admin puede desactivar un usuario."""
        update_data = {"is_active": False}
        
        response = await client.patch(
            f"/users/{ingreso_user.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
    
    async def test_update_user_email(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        consulta_user: User
    ):
        """Verifica actualización de email de usuario."""
        update_data = {"email": "nuevo_email@test.com"}
        
        response = await client.patch(
            f"/users/{consulta_user.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "nuevo_email@test.com"
    
    async def test_update_user_password(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        consulta_user: User
    ):
        """Verifica actualización de contraseña de usuario."""
        update_data = {"password": "nueva_contraseña_123"}
        
        response = await client.patch(
            f"/users/{consulta_user.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verificar que puede hacer login con nueva contraseña
        login_response = await client.post(
            "/auth/login",
            data={
                "username": consulta_user.email,
                "password": "nueva_contraseña_123"
            }
        )
        assert login_response.status_code == 200
    
    async def test_update_nonexistent_user(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que devuelve 404 al actualizar usuario inexistente."""
        update_data = {"nombre": "No existe"}
        
        response = await client.patch(
            "/users/99999",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    async def test_delete_user_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        db_session: AsyncSession
    ):
        """Verifica que admin puede eliminar un usuario."""
        # Crear usuario temporal para eliminar
        temp_user = User(
            nombre="Usuario Temporal",
            email="temp@test.com",
            hashed_password="hash",
            rol=UserRole.CONSULTA
        )
        db_session.add(temp_user)
        await db_session.commit()
        await db_session.refresh(temp_user)
        
        response = await client.delete(
            f"/users/{temp_user.id}",
            headers=admin_headers
        )
        
        assert response.status_code in [200, 204]


@pytest.mark.integration
@pytest.mark.users
@pytest.mark.asyncio
class TestUserRolePermissions:
    """Tests para verificar permisos basados en roles."""
    
    async def test_admin_can_create_users(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que admin puede crear usuarios."""
        user_data = {
            "nombre": "Nuevo Admin Created",
            "email": "admin_created@test.com",
            "password": "pass123",
            "rol": "INGRESO"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
    
    async def test_ingreso_cannot_create_users(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict
    ):
        """Verifica que INGRESO no puede crear usuarios."""
        user_data = {
            "nombre": "Intento Ingreso",
            "email": "intento@test.com",
            "password": "pass123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=ingreso_headers
        )
        
        assert response.status_code == 403
    
    async def test_consulta_cannot_create_users(
        self, 
        client: AsyncClient, 
        consulta_headers: dict
    ):
        """Verifica que CONSULTA no puede crear usuarios."""
        user_data = {
            "nombre": "Intento Consulta",
            "email": "intento2@test.com",
            "password": "pass123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=consulta_headers
        )
        
        assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.users
@pytest.mark.asyncio
class TestUserValidation:
    """Tests para validación de datos de usuario."""
    
    async def test_create_user_invalid_email(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica rechazo de email inválido."""
        user_data = {
            "nombre": "Usuario",
            "email": "email_invalido",  # No es un email válido
            "password": "pass123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=admin_headers
        )
        
        # Puede ser 422 (validation error) o 400
        assert response.status_code in [400, 422]
    
    async def test_create_user_empty_name(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica rechazo de nombre vacío."""
        user_data = {
            "nombre": "",
            "email": "test@test.com",
            "password": "pass123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=admin_headers
        )
        
        assert response.status_code in [400, 422]
    
    async def test_update_user_to_duplicate_email(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        admin_user: User,
        ingreso_user: User
    ):
        """Verifica que no se puede cambiar email a uno ya existente."""
        update_data = {"email": admin_user.email}  # Email ya existe
        
        response = await client.patch(
            f"/users/{ingreso_user.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code in [400, 409]  # Conflict


@pytest.mark.integration
@pytest.mark.users
@pytest.mark.asyncio
class TestInactiveUserBehavior:
    """Tests para comportamiento de usuarios inactivos."""
    
    async def test_inactive_user_cannot_login(
        self, 
        client: AsyncClient,
        inactive_user: User
    ):
        """Verifica que usuario inactivo no puede hacer login."""
        response = await client.post(
            "/auth/login",
            data={
                "username": inactive_user.email,
                "password": "inactive123"
            }
        )
        
        # Dependiendo de implementación, puede ser 401 o mensaje específico
        assert response.status_code == 401
    
    async def test_reactivate_user(
        self, 
        client: AsyncClient,
        admin_headers: dict,
        inactive_user: User
    ):
        """Verifica que se puede reactivar un usuario inactivo."""
        update_data = {"is_active": True}
        
        response = await client.patch(
            f"/users/{inactive_user.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is True
        
        # Verificar que ahora puede hacer login
        login_response = await client.post(
            "/auth/login",
            data={
                "username": inactive_user.email,
                "password": "inactive123"
            }
        )
        assert login_response.status_code == 200
