from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app
import pytest
from utils import DBManager, db_manager, custom_logger

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    db_manager.set_db([
        {
            "id": 3,
            "name": "test3"
        },
        {
            "id": 4,
            "name": "test4"
        }
    ])

def test_delete_device(setup_db):
    response = client.delete("/list/3")
    assert response.status_code == 200
    
    expected_response = [
        {
            "id": 4,
            "name": "test4",
        }
    ]
    assert response.json() == expected_response

