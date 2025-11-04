import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_insights_returns_dict():
    resp = client.get("/analytics/insights")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "next_tasks" in data
    assert "expense_example_category" in data
