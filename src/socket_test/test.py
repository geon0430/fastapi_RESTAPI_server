from pydantic import BaseModel
from redis.asyncio import Redis
import asyncio
import cv2
import time
import csv
from utils import setup_logger, ConfigManager

class APIstruct(BaseModel):
    id: int
    image: bytes

class DBManager:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_device(self, device_id: int) -> APIstruct:
        device_data = await self.redis.get(f"device:{device_id}")
        if device_data:
            return APIstruct(id=device_id, image=device_data)
        return None

    async def add_device(self, device: APIstruct):
        await self.redis.set(f"device:{device.id}", device.image)

    async def remove_device(self, device_id: int) -> bool:
        result = await self.redis.delete(f"device:{device_id}")
        return result > 0

    async def update_device(self, device_id: int, new_device: APIstruct) -> bool:
        if await self.redis.exists(f"device:{device_id}"):
            await self.redis.set(f"device:{device_id}", new_device.image)
            return True
        return False

async def measure_redis_speed(redis_socket_path, password, image_path, csv_file):
    redis = Redis(unix_socket_path=redis_socket_path, password=password, encoding="utf-8", decode_responses=False)
    db_manager = DBManager(redis)
    
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (1920, 1080))
    image_bytes = resized_image.tobytes()

    results = []
    for i in range(20):
        start_time = time.time()
        device = APIstruct(id=i, image=image_bytes)
        await db_manager.add_device(device)
        add_duration = time.time() - start_time

        start_time = time.time()
        retrieved_device = await db_manager.get_device(i)
        get_duration = time.time() - start_time

        results.append((len(image_bytes), add_duration, get_duration))

    await redis.close()

    total_size = results[0][0]
    average_add_duration = sum(add_duration for size, add_duration, get_duration in results) / len(results)
    average_get_duration = sum(get_duration for size, add_duration, get_duration in results) / len(results)
    print(f"File Size: {total_size} bytes, \n Average Add Duration: {average_add_duration:.6f} seconds \n Average Get Duration: {average_get_duration:.6f} seconds")

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Redis Socket Path", redis_socket_path])
        writer.writerow(["Test Number", "Image Size (bytes)", "Add Duration (seconds)", "Get Duration (seconds)"])
        for i, (size, add_duration, get_duration) in enumerate(results, 1):
            writer.writerow([f"Test {i}", size, add_duration, get_duration])

async def main():
    api_ini_path = "/fastapi_RESTAPI_server/src/config.ini"
    api_config = ConfigManager(api_ini_path)
    ini_dict = api_config.get_config_dict()
    logger = setup_logger(ini_dict)
    
    redis_password = ini_dict['REDIS']['PASSWORD']
    # redis_socket_path = ini_dict['REDIS']['SOCKET']
    redis_socket_path = "/dev/shm/redis.sock"
    
    image_path = "/fastapi_RESTAPI_server/src/0001.jpg"
    csv_file1 = "results_shm_socket.csv"
    
    await measure_redis_speed(redis_socket_path, redis_password, image_path, csv_file1)

if __name__ == "__main__":
    asyncio.run(main())
