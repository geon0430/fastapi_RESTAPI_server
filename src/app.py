from fastapi import FastAPI
import uvicorn
from redis.asyncio import Redis
from utils import setup_logger, ConfigManager, DBManager
from routers import post_router, get_router, delete_router, put_router

app = FastAPI()

app.include_router(post_router)
app.include_router(get_router)
app.include_router(delete_router)
app.include_router(put_router)

async def startup_event():
    api_ini_path = "/fastapi_RESTAPI_server/src/config.ini"
    api_config = ConfigManager(api_ini_path)
    ini_dict = api_config.get_config_dict()
    logger = setup_logger(ini_dict)
    
    host = ini_dict['REDIS']['HOST']
    port = ini_dict['REDIS']['PORT']
    password = ini_dict['REDIS']['PASSWORD']
    
    redis_url = f"redis://{host}:{port}"
    redis = Redis.from_url(redis_url, password=password, db=0, encoding="utf-8", decode_responses=True)
    
    db_manager = DBManager(redis)
    
    logger.info("DASHBOARD STARTED")

    app.state.logger = logger
    app.state.ini_dict = ini_dict
    app.state.db_manager = db_manager
    app.state.redis = redis  # 추가하여 shutdown_event에서 접근 가능하게 설정

async def shutdown_event():
    await app.state.redis.close()

app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
