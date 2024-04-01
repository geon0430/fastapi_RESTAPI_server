from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List

from utils import custom_logger, APIstruct, db_list, validate_config, db_list_check

post_router = APIRouter()

@post_router.post("/list/", status_code=status.HTTP_200_OK)
async def POST_Router(devices: List[APIstruct]):
    start_time = datetime.now() 
    
    duplicate_check_result = await db_list_check(devices)
    if duplicate_check_result:
        custom_logger.error(f"POST Router | ERROR | db_list_check Result: {duplicate_check_result}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=duplicate_check_result)

    validation_result = await validate_config(devices)
    if validation_result:
        custom_logger.error(f"POST Router | ERROR | Validation Result: {validation_result}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=validation_result)

    for device in devices:
        if device.post_time == "":
            device.post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        custom_logger.info(f"POST Router | post_time add JSON Data: {device.post_time}")
        db_list.append(device)

    elapsed_time = (datetime.now() - start_time).total_seconds()

    if elapsed_time > 2.0:
        custom_logger.error("POST Router | EEROR | TIMEOUT  Result")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    
    custom_logger.info("POST Router | JSON Data send successfully ")
    return {"message": "POST Router | JSON Data processed successfully", "devices_count": len(devices)}


    