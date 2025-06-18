import pytest
from fastapi.testclient import TestClient
from app.main import app  # ou où ton FastAPI est défini

@pytest.fixture
def client():
    return TestClient(app)