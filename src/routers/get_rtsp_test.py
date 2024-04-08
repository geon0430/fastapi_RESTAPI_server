from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app
import pytest
from utils import config_mng, custom_logger, DBManager, db_manager
client = TestClient(app)

client = TestClient(app)

def setup_module(module):
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
]
)
def test_GET_Router():
    response = client.get("/list/")
    assert response.status_code == 200
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
    ]
    assert response.json() == expected_response


def test_GET_Router_list():
    response = client.get("/list/3")
    assert response.status_code == 200
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
