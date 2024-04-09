from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import List

from utils import custom_logger, APIstruct
from utils.struct import db_manager

get_router = APIRouter()

@get_router.get("/list/", response_model=List[APIstruct])
async def get_items():
    start_time = datetime.now() 
    json_list = []

    for item in db_manager.get_db():
        json_list_data = {}
        for field in APIstruct.__fields__.keys():
            json_list_data[field] = getattr(item, field)
        
        transformed_item = APIstruct(**json_list_data)
    
        json_list.append(transformed_item)

    elapsed_time = (datetime.now() - start_time).total_seconds()
    
    if elapsed_time > 2.0:
        custom_logger.error("GET Router | ERROR | Time Out Error")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    custom_logger.info("GET Router | JSON Data send successfully ")
    return json_list

@get_router.get("/list/{id}", response_model=APIstruct)
async def get_item_by_id(id: int):
    start_time = datetime.now() 
    for item in db_manager.get_db():
        if item.id == id:
            custom_logger.info("GET Router | JSON Data send successfully ")
            return item
    elapsed_time = (datetime.now() - start_time).total_seconds()
    
    if elapsed_time > 2.0:
        custom_logger.error("GET Router | Time Out Error")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")
    
    custom_logger.error(f"GET Router | Item with id {id} not found ")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
