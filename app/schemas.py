from pydantic import BaseModel, UUID4, EmailStr
from datetime import datetime
from typing import List

class Customer(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    created_date: datetime
    is_active: bool
    country_code: str

    class Config:
        from_attributes = True # Allows Pydantic to read data from objects
