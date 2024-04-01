from fastapi.testclient import TestClient
import sys
sys.path.append("../")
from main import app

client = TestClient(app)

def test_POST_Router():
    response = client.post(
        "/list/",
        json={
            "id": 1,
            "name": "inbic01",
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
    )
    assert response.status_code == 200
    assert response.json() == {"message": "POST Router | Send JSON Data successfully", "device_id": 1}
