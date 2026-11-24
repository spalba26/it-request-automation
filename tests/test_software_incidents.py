import pytest
from fastapi.testclient import TestClient
from sqlite3 import connect, IntegrityError
from app.main import app
from app import database

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", str(test_db))

    with TestClient(app) as test_client:
        yield test_client
        
def test_create_software_incident(client):
    response = client.post("/software-incidents", json={
        "requester_id": "Employee123",
        "resource": "Excel",
        "description": "Application error",
        "impact": "high",
        "urgency": "medium"
    })
    assert response.status_code == 201
    
    data = response.json()
    
    assert data["id"] == 1
    assert data["priority"] == "HIGH"
    assert data["request_type"] == "software_incident"
    assert data["assigned_team"] == "IT Support"
    assert data["status"] == "pending"

@pytest.mark.parametrize(
    "field, value",
    [
        ("requester_id", "  "),
        ("resource", ""),
        ("description", "   "),
        ("impact", "very_high"),
        ("urgency", "critical"),
    ],
)    
def test_invalid_software_incident(client, field, value):
    incident_data = {
        "requester_id": "Employee123",
        "resource": "Excel",
        "description": "Application error",
        "impact": "high",
        "urgency": "medium"
    }
    incident_data[field] = value
    response = client.post("/software-incidents", json=incident_data)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"][1]  == field
    
def test_software_incident_persistence(client):
    connection = None
    try:
        response = client.post("/software-incidents", json={
            "requester_id": "Employee123",
            "resource": "Excel",
            "description": "Application error",
            "impact": "high",
            "urgency": "medium"
        })
        assert response.status_code == 201
        data = response.json()
        new_id = data["id"]
        connection = connect(database.DB_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT requester_id, status, assigned_team
            FROM requests
            WHERE id = ?
        """, (new_id,)
        )
        request = cursor.fetchone()
        cursor.execute("""
            SELECT resource, impact, urgency, priority
            FROM software_incidents
            WHERE request_id = ?
        """, (new_id,)
        )
        incident = cursor.fetchone()
        assert request == ("Employee123", "pending", "IT Support")
        assert incident ==  ("Excel", "high", "medium", "HIGH")
    finally:
        if connection:
            connection.close()

def test_software_incident_rollback(client):
    connection = None
    try:
        incident_data = {
            "request_type": "software_incident",
            "requester_id": "Employee123",
            "status": "pending",
            "assigned_team": "IT Support",
            "resource": None,
            "description": "Application error",
            "impact": "high",
            "urgency": "medium",
            "priority": "HIGH"
        }
        with pytest.raises(IntegrityError):
            database.insert_software_incident(incident_data)
        connection = connect(database.DB_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM requests
        """
        )
        request = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) FROM software_incidents
        """
        )
        incident = cursor.fetchone()
        assert request[0] == 0
        assert incident[0] ==  0
    finally:
        if connection:
            connection.close()