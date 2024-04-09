from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app

client = TestClient(app)

def test_POST_Router():
    response = client.post(
        "/list/",
        json=[
            {
            "id": 1,
            "name": "test",
        },
    ],
    )
    assert response.status_code == 200
    assert response.json() == {"message": "POST Router | JSON Data processed successfully"}
  