from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import re
from typing import List
from utils import config_mng, custom_logger, APIstruct,json_list, db_list

ini_dict = config_mng.get_config_dict()

async def validate_config(json_list: List[APIstruct]) -> str:
    time_format = "%H:%M"
    error_messages = []

    for config in json_list:
        try:
            datetime.strptime(config.on_time, time_format)
        except ValueError:
            error_messages.append(f"Invalid ON_TIME format: {config.on_time}")
        
        try:
            datetime.strptime(config.off_time, time_format)
        except ValueError:
            error_messages.append(f"Invalid OFF_TIME format: {config.off_time}")
        
        if not re.match("^[a-zA-Z0-9-_@.]+$", config.name):
            error_messages.append(f"Invalid NAME format: {config.name}")
        
        if not re.match("^[0-9]+$", str(config.id)):
            error_messages.append(f"Invalid ID format: {config.id}")
        
        if config.in_width > 1920 or config.in_height > 1080:
            error_messages.append("Invalid IN_WIDTH or IN_HEIGHT values")
        if config.out_width > 1920 or config.out_height > 1080:
            error_messages.append("Invalid OUT_WIDTH or OUT_HEIGHT values")
        
        if config.fps < 0 or config.fps > 30.0:
            error_messages.append("Invalid FPS value")
    
    if error_messages:
        return " | ".join(error_messages)
    
    return ""


async def db_list_check(json_list: List[APIstruct]) -> str:
    for new_item in json_list:
        for existing_item in db_list:
            if new_item.id == existing_item.id or new_item.name == existing_item.name:
                return f"Duplicate entry found with id: {new_item.id} or name: {new_item.name}"
    return ""
