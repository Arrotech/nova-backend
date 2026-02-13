from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.booking import BookingStatus
from app.schemas.car import Car

class BookingBase(BaseModel):
    car_id: int
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    car_id: int

class BookingUpdate(BaseModel):
    status: BookingStatus

class Booking(BookingBase):
    id: int
    status: str # Or BookingStatus enum
    created_at: datetime
    car: Optional[Car] = None

    class Config:
        from_attributes = True
