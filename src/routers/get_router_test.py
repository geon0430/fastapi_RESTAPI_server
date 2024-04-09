from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app
import pytest
from utils import config_mng, custom_logger, db_manager

client = TestClient(app)
@pytest.fixture(scope="module")
def setup_db():
    db_manager.set_db([
    {
            "id": 3,
            "name": "test3",
    },
     {
            "id": 4,
            "name": "test4",
    }
]
)
def test_GET_Router(setup_db):
    response = client.get("/list/")
    assert response.status_code == 200
    expected_response = [
            {
                    "id": 3,
                    "name": "test3",
            },
            {
                    "id": 4,
                    "name": "test4",
            }
    ]
    assert response.json() == expected_response


def test_GET_Router_list():
    response = client.get("/list/3")
    assert response.status_code == 200
    expected_response = {
            "id": 3,
            "name": "test3",
        }
    
    assert response.json() == expected_response
