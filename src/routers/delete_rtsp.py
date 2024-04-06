from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
import sys
sys.path.append("../")

from utils import custom_logger, APIstruct, db_list

delete_router = APIRouter()

@delete_router.delete("/list/{id}", response_model=List[APIstruct])
async def DELETE_Router(id: int):
    start_time = datetime.now()
    global db_list  
    item_to_delete = None

    for item in db_list:
        if item.id == id:
            item_to_delete = item
            break

    if item_to_delete is None:
        custom_logger.error(f"DELETE Router | Item with id {id} not found ")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
    
    db_list.remove(item_to_delete)
    db_list.sort(key=lambda item: item.id)

    elapsed_time = (datetime.now() - start_time).total_seconds()
    
    if elapsed_time > 2.0:
        custom_logger.error("DELETE Router | ERROR | Time Out Error")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request timeout")

    custom_logger.info(f"DELETE Router | Item with id {id} deleted successfully")
    return db_list
