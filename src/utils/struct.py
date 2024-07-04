from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List

class APIstruct(BaseModel):
    id: int
    name: str


class DB(BaseModel):
    id: int
    name: str
    gpu: int
