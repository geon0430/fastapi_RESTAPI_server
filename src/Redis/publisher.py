from pydantic import BaseModel
from redis.asyncio import Redis
import asyncio
import cv2
import sys
sys.path.append("../")
from src.utils import setup_logger, ConfigManager, APIstruct, DBManager
from redis.exceptions import ConnectionError

class Publisher:
    def __init__(self, api_ini_path):
        self.api_ini_path = api_ini_path
        self.api_config = ConfigManager(self.api_ini_path)
        self.ini_dict = self.api_config.get_config_dict()
        self.logger = setup_logger(self.ini_dict)
        self.redis_socket_path = self.ini_dict['REDIS']['SOCKET']
        self.password = self.ini_dict['REDIS']['PASSWORD']
        self.redis = Redis(unix_socket_path=self.redis_socket_path, password=self.password, encoding="utf-8", decode_responses=False)
        self.db_manager = DBManager(self.redis)
        self.channel = "my-channel"

    async def publish_images(self, image_path):
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (1920, 1080))
        image_bytes = resized_image.tobytes()

        for i in range(1000):
            while True:
                try:
                    device = await self.db_manager.get_device(i)
                    if device is None or device.flag == 0:
                        device = APIstruct(id=i, image=image_bytes, flag=1)
                        await self.db_manager.add_device(device)
                        await self.redis.publish(self.channel, f"{device.id}")
                        print(f"Published image {i+1} to {self.channel}")
                        break
                    else:
                        await asyncio.sleep(0.01)
                except ConnectionError as e:
                    print(f"Connection error: {e}. Retrying in 1 second...")
                    await asyncio.sleep(1)

    async def main(self):
        image_path = "/video_converter_server/src/0001.jpg"
        await self.publish_images(image_path)
        await self.redis.aclose()

if __name__ == "__main__":
    api_ini_path = "/video_converter_server/src/config.ini"
    publisher = Publisher(api_ini_path)
    asyncio.run(publisher.main())
