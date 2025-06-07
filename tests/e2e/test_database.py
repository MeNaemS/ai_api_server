import pytest
from sqlalchemy import select
from src.infrastructure.database.models.users import User
from src.infrastructure.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
async def test_create_user(db_session):
    hasher = PasswordHasher()
    hashed_password = await hasher.password_hash("testpassword")
    
    db_session.add(User(
        id=None,
        login="testdb_user",
        email="testdb@example.com",
        password=hashed_password,
        name=None,
        surname=None,
        patronymic=None,
        input_tokens=None,
        output_tokens=None
    ))
    await db_session.commit()
    
    result = await db_session.execute(select(User).where(User.login == "testdb_user"))
    user = result.scalar_one()
    
    assert user is not None
    assert user.login == "testdb_user"
    assert user.email == "testdb@example.com"
    
    await db_session.delete(user)
    await db_session.commit()


@pytest.mark.asyncio
async def test_create_user_with_tokens(db_session):
    hasher = PasswordHasher()
    hashed_password = await hasher.password_hash("testpassword")
    
    user = User(
        id=None,
        login="testdb_user_tokens",
        email="testdb_tokens@example.com",
        password=hashed_password,
        name=None,
        surname=None,
        patronymic=None,
        input_tokens=100,
        output_tokens=50
    )
    db_session.add(user)
    await db_session.commit()
    
    result = await db_session.execute(select(User).where(User.login == "testdb_user_tokens"))
    user = result.scalar_one()
    
    assert user is not None
    assert user.login == "testdb_user_tokens"
    assert user.input_tokens == 100
    assert user.output_tokens == 50
    
    await db_session.delete(user)
    await db_session.commit()
