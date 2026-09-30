import pytest
from app import create_app
from config import TestingConfig

@pytest.fixture()
def app():
    return create_app(TestingConfig)

@pytest.fixture()
def client(app):
    with app.app_context():
        from app.extensions import db
        db.create_all()
    return app.test_client()

def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
