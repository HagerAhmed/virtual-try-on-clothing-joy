import pytest
import os
import sys
from pathlib import Path

# Add the project root to python path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app import models

# Use a separate test database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # We can seed some data here if needed, or in tests
    # Let's verify clean state
    
    yield engine
    
    # Teardown
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_integration.db"):
        os.remove("./test_integration.db")

@pytest.fixture(scope="function")
def db(db_engine):
    """
    Creates a new database session for a test.
    Rolls back the transaction after the test is complete.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
