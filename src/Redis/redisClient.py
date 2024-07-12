import redis.asyncio as aioredis
import asyncio
import subprocess
import os
import sys
import cv2
import textwrap
sys.path.append("../")
from src.utils import setup_logger, ConfigManager, DBManager, APIstruct
from redis.exceptions import ConnectionError

class RedisClient:
    def __init__(self, channel, api_ini_path="/video_converter_server/src/config.ini"):
        self.channel = channel
        self.api_ini_path = api_ini_path
        self.api_config = ConfigManager(self.api_ini_path)
        self.ini_dict = self.api_config.get_config_dict()
        self.logger = setup_logger(self.ini_dict)
        self.REDIS_CONF_DIR = self.ini_dict['REDIS']['SOCKET_PATH']
        self.REDIS_CONF_PATH = os.path.join(self.REDIS_CONF_DIR, f"{channel}.conf")
        self.redis_socket_path = os.path.join(self.ini_dict['REDIS']['SOCKET_PATH'], self.ini_dict['REDIS']['SOCKET_NAME'])
        self.password = self.ini_dict['REDIS']['PASSWORD']
        self.redis_client = aioredis.Redis(unix_socket_path=self.redis_socket_path, password=self.password, encoding="utf-8", decode_responses=False)
        self.db_manager = DBManager(self.redis_client)
        self.create_redis_conf()
        self.redis_process = subprocess.Popen(['redis-server', self.REDIS_CONF_PATH],
                                              stdout=subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)

    def create_redis_conf(self):
        REDIS_CONF_CONTENT = textwrap.dedent(f"""
        protected-mode no
        bind 0.0.0.0
        requirepass {self.password}
        save ""
        appendonly no
        stop-writes-on-bgsave-error no

        port 0
        unixsocket {self.redis_socket_path}
        unixsocketperm 700
        """)
        if not os.path.exists(self.REDIS_CONF_DIR):
            os.makedirs(self.REDIS_CONF_DIR)
            print(f"Created directory: {self.REDIS_CONF_DIR}")

        if not os.path.exists(self.REDIS_CONF_PATH):
            with open(self.REDIS_CONF_PATH, 'w') as conf_file:
                conf_file.write(REDIS_CONF_CONTENT.strip())
            print(f"Created redis.conf at: {self.REDIS_CONF_PATH}")
            
    async def run(self):
        while not os.path.exists(self.redis_socket_path):
            print("Waiting for Redis socket to be created...")
            await asyncio.sleep(0.5)
        
        await self.get()

    async def get(self):
        while True:
            try:
                device_id = await self.redis_client.lpop(self.channel)
                if device_id:
                    device_id = int(device_id)
                    device = await self.db_manager.get_device(device_id)
                else:
                    await asyncio.sleep(0.1)
            except ConnectionError as e:
                print(f"Connection error: {e}. Retrying in 1 second...")
                await asyncio.sleep(1)

    async def put(self, device: APIstruct):
        try:
            await self.db_manager.add_device(device)
            await self.redis_client.rpush(self.channel, f"{device.id}")
        except ConnectionError as e:
            print(f"Connection error: {e}. Retrying in 1 second...")
            await asyncio.sleep(1)
