import pytest
from unittest.mock import MagicMock
from app.routes.salle.schemas import SalleCreate, SalleUpdate, SalleOut
from app.routes.salle import services

# Exemple de données fictives
fake_salle = SalleOut(
    id="abc123",
    nom="Salle 101",
    capacite=30,
    localisation="Bâtiment A",
    disponible=True
)

# Test POST /salle/
def test_create_salle(client, monkeypatch):
    def mock_create_salle(db, salle: SalleCreate):
        return fake_salle

    monkeypatch.setattr(services, "create_salle", mock_create_salle)

    payload = {
        "nom": "Salle 101",
        "capacite": 30,
        "localisation": "Bâtiment A",
        "disponible": True
    }

    response = client.post("/salle/", json=payload)

    assert response.status_code == 201
    assert response.json()["data"]["nom"] == "Salle 101"

# Test GET /salle/{salle_id}
def test_get_salle_by_id(client, monkeypatch):
    def mock_get_salle_by_id(db, salle_id: str):
        return fake_salle

    monkeypatch.setattr(services, "get_salle_by_id", mock_get_salle_by_id)

    response = client.get("/salle/abc123")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == "abc123"

# Test GET /salle/
def test_get_all_salles(client, monkeypatch):
    def mock_get_all_salles(db):
        return [fake_salle]

    monkeypatch.setattr(services, "get_all_salles", mock_get_all_salles)

    response = client.get("/salle/")

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert response.json()["data"][0]["id"] == "abc123"

# Test PUT /salle/{salle_id}
def test_update_salle(client, monkeypatch):
    def mock_update_salle(db, salle_id: str, salle_update: SalleUpdate):
        return fake_salle

    monkeypatch.setattr(services, "update_salle", mock_update_salle)

    update_payload = {
        "nom": "Salle 102",
        "capacite": 35
    }

    response = client.put("/salle/abc123", json=update_payload)

    assert response.status_code == 200
    assert response.json()["data"]["nom"] == "Salle 101"  # car `fake_salle` n'est pas modifié dynamiquement ici

# Test DELETE /salle/{salle_id}
def test_delete_salle(client, monkeypatch):
    def mock_delete_salle(db, salle_id: str):
        return True

    monkeypatch.setattr(services, "delete_salle", mock_delete_salle)

    response = client.delete("/salle/abc123")

    assert response.status_code == 204
    assert response.content == b""
