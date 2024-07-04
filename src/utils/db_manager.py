from utils.struct import APIstruct
import json
from redis.asyncio import Redis

class DBManager:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.key = "devices"

    async def get_db(self):
        devices = await self.redis.get(self.key)
        if devices:
            return [APIstruct(**item) for item in json.loads(devices)]
        return []

    async def add_device(self, device: APIstruct):
        devices = await self.get_db()
        devices.append(device)
        await self.redis.set(self.key, json.dumps([device.dict() for device in devices]))

    async def remove_device(self, device_id: int) -> bool:
        devices = await self.get_db()
        original_length = len(devices)
        devices = [device for device in devices if device.id != device_id]
        await self.redis.set(self.key, json.dumps([device.dict() for device in devices]))
        return len(devices) < original_length

    async def update_device(self, device_id: int, new_device: APIstruct) -> bool:
        devices = await self.get_db()
        for i, device in enumerate(devices):
            if device.id == device_id:
                devices[i] = new_device
                await self.redis.set(self.key, json.dumps([device.dict() for device in devices]))
                return True
        return False

    async def set_db(self, new_db_list):
        await self.redis.set(self.key, json.dumps([item.dict() for item in new_db_list]))

    async def get_sorted_devices(self, key: str):
        devices = await self.get_db()
        return sorted(devices, key=lambda x: getattr(x, key))
