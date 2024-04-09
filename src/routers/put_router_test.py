from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app
import pytest

client = TestClient(app)
from utils import config_mng, custom_logger, db_manager

@pytest.fixture(scope="module")
def setup_db():
    db_manager.set_db([
    {
            "id": 3,
            "name": "test3",
    }
]
)

def test_PUT_Router(setup_db):
    response = client.put(
        "/list/3",
        json={
            "id": 3,
            "name": "test5",
        },
    )
    assert response.status_code == 200
    expected_response = {
        "id": 3,
        "name": "test5",
    }
    
    assert response.json() == expected_response
