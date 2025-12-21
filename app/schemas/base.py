# app/schemas/base.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class BaseCreateSchema(BaseSchema):
    pass

class BaseUpdateSchema(BaseSchema):
    pass