import re
from typing import List
from utils import APIstruct
 
async def validate_config(json_list: List[APIstruct]) -> str:
    time_format = "%H:%M"
    error_messages = []

    for config in json_list:
        # try:
        #     datetime.strptime(config._time, time_format)
        # except ValueError:
        #     error_messages.append(f"Invalid TIME format: {config.on_time}")
        
        if not re.match("^[a-zA-Z0-9-_@.]+$", config.name):
            error_messages.append(f"Invalid NAME format: {config.name}")
        
        if not re.match("^[0-9]+$", str(config.id)):
            error_messages.append(f"Invalid ID format: {config.id}")
        
        # if config.in_width > 1920 or config.in_height > 1080:
        #     error_messages.append("Invalid IN_WIDTH or IN_HEIGHT values")


    if error_messages:
        return " | ".join(error_messages)
    
    return ""


async def db_list_check(devices, db_manager):
    existing_devices = await db_manager.get_db()  # Await the coroutine
    for existing_item in existing_devices:
        for new_item in devices:
            if existing_item.id == new_item.id:
                return f"Duplicate device id found: {existing_item.id}"
    return None
