from fastapi import APIRouter, HTTPException, status, Body
from typing import List
from datetime import datetime

from utils import custom_logger, APIstruct, db_list_check, validate_config
from utils.struct import db_manager

put_router = APIRouter()

@put_router.put("/list/{id}", response_model=APIstruct)
async def PUT_Router(id: int, device: APIstruct):
    start_time = datetime.now()
    existing_device = next((d for d in db_manager.get_db() if d.id == id), None)
    if not existing_device:
        custom_logger.error(f"PUT Router | ERROR | No existing device with id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existing device with id: {id}")

    success = db_manager.update_device(id, device)
    if not success:
        custom_logger.error(f"PUT Router | ERROR | Failed to update device with id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to update device with id: {id}")

    custom_logger.info(f"PUT Router | Device with id {id} updated successfully")

    elapsed_time = (datetime.now() - start_time).total_seconds()
    if elapsed_time > 2.0:
        custom_logger.error("PUT Router | ERROR | TIMEOUT Result")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    
    custom_logger.info("PUT Router | JSON Data update successfully")
    return device
