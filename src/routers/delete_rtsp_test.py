from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app
import pytest
from utils import DBManager, db_manager

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    db_manager.set_db([
        {
            "id": 3,
            "name": "inbic03",
            "rtsp": "rtsp://admin:qazwsx123!@192.168.10.70/0/1080p/media.smp",
            "codec": "h264",
            "model": "NOX",
            "fps": 30.0,
            "in_width": 1920,
            "in_height": 1080,
            "out_width": 720,
            "out_height": 480,
            "on_time": "18:00",
            "off_time": "02:42",
            "button": False,
            "random_seed": 1234,
            "post_time": "2024-03-27 10:27:29",
            "update_time": "",
            "status": "starting"
        },
        {
            "id": 4,
            "name": "inbic04",
            "rtsp": "rtsp://admin:qazwsx123!@192.168.10.70/0/1080p/media.smp",
            "codec": "h264",
            "model": "NOX",
            "fps": 30.0,
            "in_width": 1920,
            "in_height": 1080,
            "out_width": 720,
            "out_height": 480,
            "on_time": "18:00",
            "off_time": "02:42",
            "button": False,
            "random_seed": 1234,
            "post_time": "",
            "update_time": "",
            "status": "starting"
        }
    ])

def test_delete_device(setup_db):
    response = client.delete("/list/4")
    assert response.status_code == 200
    
    response = client.get("/list/")
    expected_response = [
        {
            "id": 3,
            "name": "inbic03",
            "rtsp": "rtsp://admin:qazwsx123!@192.168.10.70/0/1080p/media.smp",
            "codec": "h264",
            "model": "NOX",
            "fps": 30.0,
            "in_width": 1920,
            "in_height": 1080,
            "out_width": 720,
            "out_height": 480,
            "on_time": "18:00",
            "off_time": "02:42",
            "button": False,
            "random_seed": 1234,
            "post_time": "2024-03-27 10:27:29",
            "update_time": "",
            "status": "starting"
        }
    ]
    assert response.json() == expected_response

