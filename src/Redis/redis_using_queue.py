import redis.asyncio as aioredis
import asyncio
import subprocess
import os
import sys
import cv2
import numpy as np
import csv
from datetime import datetime

sys.path.append("../")
from Redis.redisClient import RedisClient
from src.utils import setup_logger, ConfigManager, DBManager, APIstruct

async def datasend(data_queue, logger, time_dict):
    image_path = "/video_converter_server/src/0001.jpg"
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (1920, 1080))
    image_bytes = resized_image.tobytes()

    for device_id in range(1, 1001):
        device = APIstruct(id=device_id, image=image_bytes, flag=1)
        await data_queue.put(device)
        send_time = datetime.now().timestamp()
        time_dict[device_id] = send_time
        logger.info(f"Published device {device.id} to {data_queue.channel}")

async def datasave(data_queue, logger, time_dict):
    processed_devices = 0
    while processed_devices < 1000:
        device_id = await data_queue.redis_client.lpop(data_queue.channel)
        if device_id:
            device_id = int(device_id)
            device = await data_queue.db_manager.get_device(device_id)
            if device:
                receive_time = datetime.now().timestamp()
                send_time = time_dict[device_id]
                duration = receive_time - send_time

                print(f"Received device {device.id}, image length: {len(device.image)}")

                image_array = np.frombuffer(device.image, dtype=np.uint8).reshape((1080, 1920, 3))
                cv2.imwrite(f"./test/result_{device.id}.jpg", image_array)
                logger.info(f"Image saved as ./test/result_{device.id}.jpg")

                time_dict[device_id] = duration
                processed_devices += 1

async def main():
    channel = "my-channel"
    data_queue = RedisClient(channel)
    api_ini_path = "/video_converter_server/src/config.ini"
    api_config = ConfigManager(api_ini_path)
    ini_dict = api_config.get_config_dict()
    logger = setup_logger(ini_dict)
    
    time_dict = {}
    
    send_task = asyncio.create_task(datasend(data_queue, logger, time_dict))
    save_task = asyncio.create_task(datasave(data_queue, logger, time_dict))

    await send_task
    await save_task

    with open('./times.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["device_id", "duration"])
        for device_id, duration in time_dict.items():
            writer.writerow([device_id, duration])

if __name__ == "__main__":
    asyncio.run(main())
