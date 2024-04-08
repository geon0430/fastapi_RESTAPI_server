from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class DBManager:
    def __init__(self):
        self.db_list = []  

    def get_db(self):
        return self.db_list  
    
    def add_device(self, device):
        self.db_list.append(device) 

    def remove_device(self, device_id):
        self.db_list = [device for device in self.db_list if device.id != device_id] 

    def update_device(self, device_id, new_device):
        for i, device in enumerate(self.db_list):
            if device.id == device_id:
                self.db_list[i] = new_device
                return True  
        return False


class APIstruct(BaseModel):
    id: int
    name: str
    rtsp: str
    codec: str
    model: str
    fps: float
    in_width: int
    in_height: int
    out_width: int
    out_height: int
    on_time: str
    off_time: str
    post_time: str
    update_time: str
    status: str
    button: bool
    random_seed: int

json_list: List[APIstruct] = []

class DB(BaseModel):
    id: int
    name: str
    rtsp: str
    codec: str
    model: str
    fps: float
    in_width: int
    in_height: int
    out_width: int
    out_height: int
    on_time: str
    off_time: str
    post_time: str
    update_time: str
    status: str
    button: bool
    random_seed: int
    gpu: int
    moniter: bool

db_list: List[DB] = []
