"""
Tests de integración para endpoints de autenticación.
Prueba login, registro, cambio de contraseña y obtención de usuario actual.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserRole


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.asyncio
class TestAuthenticationEndpoints:
    """Tests para endpoints de autenticación."""
    
    async def test_login_success(self, client: AsyncClient, admin_user: User):
        """Verifica login exitoso con credenciales correctas."""
        response = await client.post(
            "/auth/login",
            data={
                "username": admin_user.email,
                "password": "admin123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    async def test_login_wrong_password(self, client: AsyncClient, admin_user: User):
        """Verifica que login falla con contraseña incorrecta."""
        response = await client.post(
            "/auth/login",
            data={
                "username": admin_user.email,
                "password": "wrong_password"
            }
        )
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Verifica que login falla con usuario inexistente."""
        response = await client.post(
            "/auth/login",
            data={
                "username": "nonexistent@test.com",
                "password": "anypassword"
            }
        )
        
        assert response.status_code == 401
    
    async def test_login_empty_credentials(self, client: AsyncClient):
        """Verifica que login falla con credenciales vacías."""
        response = await client.post(
            "/auth/login",
            data={
                "username": "",
                "password": ""
            }
        )
        
        assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.asyncio
class TestUserRegistration:
    """Tests para registro de usuarios."""
    
    async def test_register_user_as_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que un admin puede registrar un nuevo usuario."""
        user_data = {
            "nombre": "Nuevo Usuario",
            "email": "nuevo@test.com",
            "password": "password123",
            "rol": "INGRESO"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Nuevo Usuario"
        assert data["email"] == "nuevo@test.com"
        assert data["rol"] == "INGRESO"
        assert "hashed_password" not in data
        assert "password" not in data
    
    async def test_register_user_as_non_admin(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict
    ):
        """Verifica que un usuario no-admin no puede registrar usuarios."""
        user_data = {
            "nombre": "Nuevo Usuario",
            "email": "nuevo2@test.com",
            "password": "password123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=ingreso_headers
        )
        
        assert response.status_code == 403
        assert "Only admins can register users" in response.json()["detail"]
    
    async def test_register_duplicate_email(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        admin_user: User
    ):
        """Verifica que no se puede registrar un email duplicado."""
        user_data = {
            "nombre": "Duplicado",
            "email": admin_user.email,  # Email ya existe
            "password": "password123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data,
            headers=admin_headers
        )
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    async def test_register_without_authentication(self, client: AsyncClient):
        """Verifica que no se puede registrar sin autenticación."""
        user_data = {
            "nombre": "Sin Auth",
            "email": "sinauth@test.com",
            "password": "password123",
            "rol": "CONSULTA"
        }
        
        response = await client.post(
            "/auth/register",
            json=user_data
        )
        
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.asyncio
class TestGetCurrentUser:
    """Tests para obtener información del usuario actual."""
    
    async def test_get_current_user_admin(
        self, 
        client: AsyncClient, 
        admin_headers: dict,
        admin_user: User
    ):
        """Verifica que se puede obtener información del usuario admin actual."""
        response = await client.get(
            "/auth/me",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == admin_user.email
        assert data["nombre"] == admin_user.nombre
        assert data["rol"] == UserRole.ADMIN.value
        assert data["is_active"] is True
    
    async def test_get_current_user_ingreso(
        self, 
        client: AsyncClient, 
        ingreso_headers: dict,
        ingreso_user: User
    ):
        """Verifica que se puede obtener información del usuario ingreso actual."""
        response = await client.get(
            "/auth/me",
            headers=ingreso_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == ingreso_user.email
        assert data["rol"] == UserRole.INGRESO.value
    
    async def test_get_current_user_without_auth(self, client: AsyncClient):
        """Verifica que no se puede obtener usuario sin autenticación."""
        response = await client.get("/auth/me")
        
        assert response.status_code == 401
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Verifica que falla con token inválido."""
        response = await client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.asyncio
class TestPasswordChange:
    """Tests para cambio de contraseña."""
    
    async def test_change_password_success(
        self, 
        client: AsyncClient, 
        admin_user: User,
        admin_headers: dict
    ):
        """Verifica cambio exitoso de contraseña."""
        password_data = {
            "current_password": "admin123",
            "new_password": "new_password_456"
        }
        
        response = await client.post(
            "/auth/change-password",
            json=password_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert "Password updated successfully" in response.json()["message"]
        
        # Verificar que puede hacer login con la nueva contraseña
        login_response = await client.post(
            "/auth/login",
            data={
                "username": admin_user.email,
                "password": "new_password_456"
            }
        )
        assert login_response.status_code == 200
    
    async def test_change_password_wrong_current(
        self, 
        client: AsyncClient, 
        admin_headers: dict
    ):
        """Verifica que falla con contraseña actual incorrecta."""
        password_data = {
            "current_password": "wrong_password",
            "new_password": "new_password_456"
        }
        
        response = await client.post(
            "/auth/change-password",
            json=password_data,
            headers=admin_headers
        )
        
        assert response.status_code == 400
        assert "Incorrect current password" in response.json()["detail"]
    
    async def test_change_password_without_auth(self, client: AsyncClient):
        """Verifica que no se puede cambiar contraseña sin autenticación."""
        password_data = {
            "current_password": "admin123",
            "new_password": "new_password"
        }
        
        response = await client.post(
            "/auth/change-password",
            json=password_data
        )
        
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.auth
@pytest.mark.asyncio
class TestAuthenticationFlow:
    """Tests de flujo completo de autenticación."""
    
    async def test_full_authentication_flow(
        self, 
        client: AsyncClient,
        admin_user: User,
        admin_headers: dict
    ):
        """Verifica el flujo completo: registro, login, obtener usuario."""
        # 1. Registrar nuevo usuario
        user_data = {
            "nombre": "Usuario Completo",
            "email": "completo@test.com",
            "password": "password123",
            "rol": "INGRESO"
        }
        
        register_response = await client.post(
            "/auth/register",
            json=user_data,
            headers=admin_headers
        )
        assert register_response.status_code == 200
        
        # 2. Login con el nuevo usuario
        login_response = await client.post(
            "/auth/login",
            data={
                "username": "completo@test.com",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # 3. Obtener información del usuario
        me_response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        user_info = me_response.json()
        assert user_info["email"] == "completo@test.com"
        assert user_info["rol"] == "INGRESO"
