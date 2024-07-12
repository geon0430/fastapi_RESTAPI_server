import redis.asyncio as aioredis
import asyncio
import subprocess
import os
import time
import numpy as np
import cv2
from datetime import datetime
import sys
sys.path.append("../")
from src.utils import setup_logger, ConfigManager, DBManager, APIstruct
from redis.exceptions import ConnectionError

class RedisClient:
    REDIS_CONF_DIR = "/video_converter_server/Redis"
    REDIS_CONF_PATH = os.path.join(REDIS_CONF_DIR, "redis.conf")
    IMAGE_SAVE_DIR = "./test"

    def __init__(self, api_ini_path):
        self.api_ini_path = api_ini_path
        self.api_config = ConfigManager(self.api_ini_path)
        self.ini_dict = self.api_config.get_config_dict()
        self.logger = setup_logger(self.ini_dict)
        self.redis_socket_path = self.ini_dict['REDIS']['SOCKET']
        self.password = self.ini_dict['REDIS']['PASSWORD']
        self.channel = "my-channel"
        self.redis_client = aioredis.Redis(unix_socket_path=self.redis_socket_path, password=self.password, encoding="utf-8", decode_responses=False)
        self.db_manager = DBManager(self.redis_client)
        self.last_time = None

        if not os.path.exists(self.IMAGE_SAVE_DIR):
            os.makedirs(self.IMAGE_SAVE_DIR)
            print(f"Created directory: {self.IMAGE_SAVE_DIR}")

    def create_redis_conf(self):
        REDIS_CONF_CONTENT = f"""
        protected-mode no
        bind 0.0.0.0
        requirepass {self.password}
        save ""
        appendonly no
        stop-writes-on-bgsave-error no

        port 0
        unixsocket {self.redis_socket_path}
        unixsocketperm 700
        """
        if not os.path.exists(self.REDIS_CONF_DIR):
            os.makedirs(self.REDIS_CONF_DIR)
            print(f"Created directory: {self.REDIS_CONF_DIR}")

        if not os.path.exists(self.REDIS_CONF_PATH):
            with open(self.REDIS_CONF_PATH, 'w') as conf_file:
                conf_file.write(REDIS_CONF_CONTENT.strip())
            print(f"Created redis.conf at: {self.REDIS_CONF_PATH}")

    async def listen_to_channel(self):
        while True:
            try:
                pubsub = self.redis_client.pubsub()
                await pubsub.subscribe(self.channel)
                
                print(f"Subscribed to {self.channel}")

                async for message in pubsub.listen():
                    if message['type'] == 'message' and message['data'] is not None:
                        try:
                            current_time = datetime.now()
                            if self.last_time:
                                time_diff = (current_time - self.last_time).total_seconds()
                            else:
                                time_diff = None
                            self.last_time = current_time

                            device_id = int(message['data'])
                            device = await self.db_manager.get_device(device_id)
                            if device:
                                image_len = len(device.image)
                                print(f"device_id: {device_id}, image_len: {image_len}, flag: {device.flag}, time_diff: {time_diff}")

                                image_array = np.frombuffer(device.image, dtype=np.uint8).reshape((1080, 1920, 3))
                                image_path = os.path.join(self.IMAGE_SAVE_DIR, f"result_{device_id}.jpg")
                                cv2.imwrite(image_path, image_array)
                                print(f"Image {device_id} saved as {image_path}")

                                await self.db_manager.update_device(device_id, APIstruct(id=device_id, image=b"", flag=0))
                        except ValueError as ve:
                            print(f"ValueError: {ve}")
            except ConnectionError as e:
                print(f"Connection error: {e}. Retrying in 1 second...")
                await asyncio.sleep(1)

    async def main(self):
        while not os.path.exists(self.redis_socket_path):
            print("Waiting for Redis socket to be created...")
            time.sleep(0.5)

        await self.listen_to_channel()

    def start_redis_server(self):
        self.create_redis_conf()
        self.redis_process = subprocess.Popen(['redis-server', self.REDIS_CONF_PATH])

    def run(self):
        self.start_redis_server()
        try:
            asyncio.run(self.main())
        finally:
            self.redis_process.terminate()
            self.redis_process.wait()

if __name__ == "__main__":
    api_ini_path = "/video_converter_server/src/config.ini"
    subscriber = RedisClient(api_ini_path)
    subscriber.run()
