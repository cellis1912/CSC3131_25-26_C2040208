import pytest
from unittest.mock import MagicMock, patch
from app import app, get_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# --- Helper: mock DB cursor + connection ---
class MockCursor:
    def __init__(self, return_value=None):
        self.return_value = return_value or []

    def execute(self, *args, **kwargs):
        pass

    def fetchall(self):
        return self.return_value

    def fetchone(self):
        return [1]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

class MockDB:
    def cursor(self):
        return MockCursor()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


# ---------------------
#       TESTS
# ---------------------

@patch("app.db_connect", return_value=MockDB())
def test_health(mock_db, client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


@patch("app.db_connect", return_value=MockDB())
def test_metrics(mock_db, client):
    res = client.get("/metrics")
    assert res.status_code == 200
    assert b"flask_request_total" in res.data


@patch("app.db_connect", return_value=MockDB())
def test_index(mock_db, client):
    res = client.get("/")
    assert res.status_code == 200


@patch("app.db_connect", return_value=MockDB())
def test_jobs(mock_db, client):
    res = client.get("/jobs")
    assert res.status_code == 200


@patch("app.db_connect", return_value=MockDB())
def test_add_job_success(mock_db, client):
    data = {
        "title": "Test Job",
        "person": "Alice",
        "time": "3.5"
    }
    res = client.post("/add-job", data=data)
    assert res.status_code == 201
    assert res.json["message"] == "Job added successfully"


@patch("app.db_connect", return_value=MockDB())
def test_add_job_missing_fields(mock_db, client):
    res = client.post("/add-job", data={})
    assert res.status_code == 400
    assert "error" in res.json


@patch("app.db_connect", return_value=MockDB())
def test_delete_job(mock_db, client):
    res = client.post("/jobs/delete/1")
    assert res.status_code == 200
    assert res.json["success"] is True


@patch("app.db_connect", return_value=MockDB())
def test_edit_job(mock_db, client):
    data = {
        "title": "New Title",
        "person": "Bob",
        "time_estimate": "5"
    }
    res = client.post("/jobs/edit/1", data=data)
    assert res.status_code == 200
    assert res.json["success"] is True
