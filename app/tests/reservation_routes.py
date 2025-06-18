from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.routes.reservation.schemas import ReservationOut
import datetime

# On mocke get_db pour éviter les appels à la vraie base
from app.lib.db.dependencies import get_db

client = TestClient(app)

# Valeurs factices pour les tests
fake_reservation = ReservationOut(
    id="123",
    salle_id="salle_1",
    date=datetime.date(2025, 6, 18),
    heure=datetime.time(14, 0),
    utilisateur="John Doe"
)


# Override la dépendance à get_db
def override_get_db():
    db = MagicMock()
    db.begin = lambda: None
    yield db

app.dependency_overrides[get_db] = override_get_db


def test_create_reservation(monkeypatch):
    def mock_create_reservation(db, reservation_data):
        return fake_reservation

    monkeypatch.setattr("app.routes.reservation.services.create_reservation", mock_create_reservation)

    response = client.post("/reservation/", json={
        "salle_id": "salle_1",
        "date": "2025-06-18",
        "heure": "14:00:00",
        "utilisateur": "John Doe"
    })

    assert response.status_code == 201
    assert response.json()["data"]["salle_id"] == "salle_1"


def test_get_reservation(monkeypatch):
    def mock_get_reservation_by_id(db, reservation_id):
        return fake_reservation

    monkeypatch.setattr("app.routes.reservation.services.get_reservation_by_id", mock_get_reservation_by_id)

    response = client.get("/reservation/123")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == "123"


def test_get_all_reservations(monkeypatch):
    def mock_get_all_reservations(db):
        return [fake_reservation]

    monkeypatch.setattr("app.routes.reservation.services.get_all_reservations", mock_get_all_reservations)

    response = client.get("/reservation/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_update_reservation(monkeypatch):
    def mock_update_reservation(db, reservation_id, reservation_update):
        return fake_reservation

    monkeypatch.setattr("app.routes.reservation.services.update_reservation", mock_update_reservation)

    response = client.put("/reservation/123", json={
        "utilisateur": "John Doe"
    })

    assert response.status_code == 200
    assert response.json()["data"]["id"] == "123"


def test_delete_reservation(monkeypatch):
    def mock_delete_reservation(db, reservation_id):
        return True

    monkeypatch.setattr("app.routes.reservation.services.delete_reservation", mock_delete_reservation)

    response = client.delete("/reservation/123")
    assert response.status_code == 204
