import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock

from src.application.user_cases.auth_user_case import AuthService
from src.domain.models.user import UserInDB, AuthUser, RegisterUser, FullName
from src.domain.models.token import Token
from src.application.ports.auth_repository import AuthRepository
from src.infrastructure.security.password_hasher import PasswordHasher
from config.schema import Config, JWTData


@pytest.fixture
def jwt_config():
    jwt_data = MagicMock(spec=JWTData)
    jwt_data.secret_key = "test_secret_key"
    jwt_data.algorithm = "HS256"
    jwt_data.expire = 30
    return jwt_data


@pytest.fixture
def config(jwt_config):
    config = MagicMock(spec=Config)
    config.jwt = jwt_config
    return config


@pytest.fixture
def auth_repo():
    repo = AsyncMock(spec=AuthRepository)
    return repo


@pytest.fixture
def password_hasher():
    hasher = AsyncMock(spec=PasswordHasher)
    return hasher


@pytest_asyncio.fixture
async def auth_service(auth_repo, config, password_hasher):
    return AuthService(auth_repo, config, password_hasher)


@pytest.mark.asyncio
async def test_login_user_success(auth_service, auth_repo, password_hasher):
    # Arrange
    user = AuthUser(login="testuser", password="password123")
    user_in_db = UserInDB(
        id=1,
        login="testuser",
        email="test@example.com",
        full_name=None,
        password="hashed_password",
        input_tokens=None,
        output_tokens=None
    )
    
    auth_repo.get_user_in_db_by_login.return_value = user_in_db
    password_hasher.verify_password.return_value = True
    
    # Act
    result = await auth_service.login_user(user)
    
    # Assert
    assert result is not None
    assert isinstance(result, Token)
    assert result.token_type == "bearer"
    assert result.expire == auth_service.config.jwt.expire
    auth_repo.get_user_in_db_by_login.assert_called_once_with(user.login)
    password_hasher.verify_password.assert_called_once_with(user.password, user_in_db.password)


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(auth_service, auth_repo, password_hasher):
    # Arrange
    user = AuthUser(login="testuser", password="wrong_password")
    user_in_db = UserInDB(
        id=1,
        login="testuser",
        email="test@example.com",
        full_name=None,
        password="hashed_password",
        input_tokens=None,
        output_tokens=None
    )
    
    auth_repo.get_user_in_db_by_login.return_value = user_in_db
    password_hasher.verify_password.return_value = False
    
    # Act
    result = await auth_service.login_user(user)
    
    # Assert
    assert result is None
    auth_repo.get_user_in_db_by_login.assert_called_once_with(user.login)
    password_hasher.verify_password.assert_called_once_with(user.password, user_in_db.password)


@pytest.mark.asyncio
async def test_login_user_not_found(auth_service, auth_repo):
    # Arrange
    user = AuthUser(login="nonexistent", password="password123")
    auth_repo.get_user_in_db_by_login.return_value = None
    
    # Act
    result = await auth_service.login_user(user)
    
    # Assert
    assert result is None
    auth_repo.get_user_in_db_by_login.assert_called_once_with(user.login)


@pytest.mark.asyncio
async def test_register_user(auth_service, auth_repo):
    # Arrange
    full_name = FullName(name="John", surname="Doe")
    register_user = RegisterUser(
        login="newuser",
        email="new@example.com",
        full_name=full_name,
        password="password123"
    )
    
    user_in_db = UserInDB(
        id=1,
        login="newuser",
        email="new@example.com",
        full_name=1,
        password="hashed_password",
        input_tokens=None,
        output_tokens=None
    )
    
    auth_repo.create_user_in_db.return_value = user_in_db
    
    # Act
    result = await auth_service.register_user(register_user)
    
    # Assert
    assert result is not None
    assert isinstance(result, Token)
    assert result.token_type == "bearer"
    assert result.expire == auth_service.config.jwt.expire
    auth_repo.create_user_in_db.assert_called_once_with(register_user)


@pytest.mark.asyncio
async def test_create_access_token(auth_service, config):
    # Arrange
    data = {"sub": 1}
    
    # Act
    token = await auth_service._create_access_token(data)
    
    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
