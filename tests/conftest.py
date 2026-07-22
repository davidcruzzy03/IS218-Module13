"""Shared pytest fixtures for database integration tests."""

import os
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.models.calculation import Calculation


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/calculator_test_db",
)


@pytest.fixture(scope="session")
def engine():
    """Create the SQLAlchemy test engine."""

    test_engine = create_engine(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=test_engine)

    yield test_engine

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture()
def db_session(engine):
    """Provide a clean database session for each test."""

    testing_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = testing_session()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def test_user(db_session):
    """Create a database user for calculation tests."""

    unique_value = uuid.uuid4().hex[:8]

    user = User(
        email=f"test-{unique_value}@example.com",
        username=f"testuser-{unique_value}",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    yield user

    db_session.delete(user)
    db_session.commit()