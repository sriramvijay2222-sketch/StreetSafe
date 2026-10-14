import os, tempfile
from pathlib import Path
from uuid import uuid4

TEST_DATABASE = Path(tempfile.gettempdir()) / f"streetsafe-test-{uuid4().hex}.db"
os.environ["STREETSAFE_DATABASE_URL"] = f"sqlite:///{TEST_DATABASE.as_posix()}"
os.environ["ADMIN_API_KEY"] = "test-key"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app.services import haversine_m, priority

client = TestClient(app)
payload = {"category":"open drain","title":"Unsafe open drain","description":"An open drain beside the footpath.","severity":"high","latitude":16.306,"longitude":80.436}

@pytest.fixture(scope="session", autouse=True)
def remove_test_database():
    yield
    engine.dispose()
    TEST_DATABASE.unlink(missing_ok=True)


def test_health(): assert client.get("/api/health").json()["status"] == "ok"
def test_database_is_isolated(): assert "streetsafe-test-" in str(engine.url)
def test_priority_and_distance():
    assert priority("exposed electrical wire", "high")[:2] == (100, "high")
    assert haversine_m(16.306,80.436,16.306,80.436) == 0
def test_create_retrieve_and_validation():
    r = client.post("/api/reports", json=payload); assert r.status_code == 201
    incident = r.json()["incident_id"]
    assert client.get(f"/api/reports/{incident}").status_code == 200
    assert client.post("/api/reports", json={**payload,"latitude":100}).status_code == 422
def test_auth_status_and_history():
    incident = client.post("/api/reports", json={**payload,"title":"Another drain"}).json()["incident_id"]
    assert client.patch(f"/api/reports/{incident}/status", json={"status":"resolved"}).status_code == 401
    assert client.patch(f"/api/reports/{incident}/status", json={"status":"resolved","note":"Reviewed"}, headers={"X-Admin-Key":"test-key"}).status_code == 200
    assert client.get(f"/api/reports/{incident}/history").status_code == 401
    history = client.get(f"/api/reports/{incident}/history", headers={"X-Admin-Key":"test-key"}).json(); assert history[0]["new_status"] == "resolved"
