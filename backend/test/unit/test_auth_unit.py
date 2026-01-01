"""
Tests unitarios del módulo de autenticación.

Cubre:
- Hash y verificación de contraseñas
- Creación de tokens JWT
- Inclusión de claims y expiración
- Casos extremos de autenticación
"""

from datetime import timedelta

import pytest
from jose import jwt

from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)

# -----------------------------
# Constantes de test
# -----------------------------
TEST_EMAIL = "user@example.com"
TEST_PASSWORD = "test_password_123"
WRONG_PASSWORD = "wrong_password"


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def hashed_password():
    """Devuelve un hash válido para una contraseña conocida."""
    return get_password_hash(TEST_PASSWORD)


@pytest.fixture
def jwt_payload():
    """Payload base para tokens JWT."""
    return {"sub": TEST_EMAIL}


# -----------------------------
# Password hashing
# -----------------------------
@pytest.mark.unit
@pytest.mark.auth
class TestPasswordHashing:
    """
    Tests de hash y verificación de contraseñas.

    Verifica:
    - Generación de hash bcrypt
    - Uso de salt
    - Validación correcta / incorrecta
    """

    def test_generates_valid_bcrypt_hash(self):
        hashed = get_password_hash(TEST_PASSWORD)

        assert hashed
        assert hashed != TEST_PASSWORD
        assert hashed.startswith("$2b$")

    def test_same_password_generates_different_hashes(self):
        hash1 = get_password_hash(TEST_PASSWORD)
        hash2 = get_password_hash(TEST_PASSWORD)

        assert hash1 != hash2

    def test_verify_correct_password_returns_true(self, hashed_password):
        assert verify_password(TEST_PASSWORD, hashed_password) is True

    def test_verify_wrong_password_returns_false(self, hashed_password):
        assert verify_password(WRONG_PASSWORD, hashed_password) is False

    def test_verify_empty_password_returns_false(self, hashed_password):
        assert verify_password("", hashed_password) is False


# -----------------------------
# JWT token creation
# -----------------------------
@pytest.mark.unit
@pytest.mark.auth
class TestTokenCreation:
    """
    Tests de creación y contenido de tokens JWT.

    Verifica:
    - Token válido
    - Claims obligatorios
    - Expiración
    """

    def test_create_access_token_returns_string(self, jwt_payload):
        token = create_access_token(jwt_payload)

        assert isinstance(token, str)
        assert token

    def test_create_access_token_with_custom_expiry(self, jwt_payload):
        token = create_access_token(
            jwt_payload,
            expires_delta=timedelta(minutes=30),
        )

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == TEST_EMAIL
        assert "exp" in payload

    def test_token_contains_subject_claim(self, jwt_payload):
        token = create_access_token(jwt_payload)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == TEST_EMAIL

    def test_token_supports_additional_claims(self):
        data = {
            "sub": TEST_EMAIL,
            "role": "ADMIN",
            "user_id": 123,
        }

        token = create_access_token(data)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["role"] == "ADMIN"
        assert payload["user_id"] == 123

    def test_token_always_includes_expiration(self, jwt_payload):
        token = create_access_token(jwt_payload)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert isinstance(payload.get("exp"), int)


# -----------------------------
# Edge cases
# -----------------------------
@pytest.mark.unit
@pytest.mark.auth
class TestAuthenticationEdgeCases:
    """
    Tests de escenarios límite en autenticación.
    """

    def test_very_long_password_is_supported(self):
        long_password = "a" * 1000
        hashed = get_password_hash(long_password)

        assert verify_password(long_password, hashed) is True

    def test_special_characters_password_is_supported(self):
        password = "P@ssw0rd!#$%^&*()_+-=[]{}|;:',.<>?/~`"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_unicode_password_is_supported(self):
        password = "contraseña_española_ñ_áéíóú_🔒"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_token_allows_empty_subject(self):
        token = create_access_token({"sub": ""})
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert payload["sub"] == ""