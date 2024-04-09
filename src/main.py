from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
import uvicorn

from utils import config_mng, custom_logger
from routers import post_router, get_router, delete_router, put_router
import routers

ini_dict = config_mng.get_config_dict()
MAIN_PORT = int(ini_dict['DASHBOARD_CLIENT']['main_port'])
HOST_ADDRESS = ini_dict['DASHBOARD_CLIENT']['host_address']

app = FastAPI()

app.include_router(post_router)
app.include_router(get_router)
app.include_router(delete_router)
app.include_router(put_router)

if __name__ == "__main__":
    custom_logger.info("DASHBOARD STARTED")
    uvicorn.run(
            app, 
            host=HOST_ADDRESS, 
            port=MAIN_PORT,
        )