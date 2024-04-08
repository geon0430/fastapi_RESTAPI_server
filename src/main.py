from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

import uvicorn

from utils import config_mng, custom_logger, DBManager
from routers import post_router, get_router, delete_router
import routers

ini_dict = config_mng.get_config_dict()
MAIN_PORT = int(ini_dict['DASHBOARD_CLIENT']['main_port'])
HOST_ADDRESS = ini_dict['DASHBOARD_CLIENT']['host_address']

app = FastAPI()

DBManager = db_manager

def get_db_manager():
    return db_manager

@app.get("/list/")
async def get_list(db_manager: DBManager = Depends(get_db_manager)):
    return db_manager.get_db()

app.include_router(post_router)
app.include_router(get_router)
app.include_router(delete_router)

if __name__ == "__main__":
    custom_logger.info("DASHBOARD STARTED")
    uvicorn.run(
            app, 
            host=HOST_ADDRESS, 
            port=MAIN_PORT,
        )
