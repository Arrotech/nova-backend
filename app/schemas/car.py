from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class CarImageBase(BaseModel):
    image_url: str

class CarImageCreate(CarImageBase):
    pass

class CarImage(CarImageBase):
    id: int
    car_id: int
    class Config:
        from_attributes = True

class CarBase(BaseModel):
    make: str
    model: str
    year: int
    price_per_day: int
    is_available: bool = True
    description: Optional[str] = None
    features: Optional[List[str]] = []
    specs: Optional[Dict[str, Any]] = {}
    primary_image_url: Optional[str] = None

class CarCreate(CarBase):
    images: Optional[List[str]] = []

class CarUpdate(CarBase):
    images: Optional[List[str]] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price_per_day: Optional[int] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    specs: Optional[Dict[str, Any]] = None
    is_available: Optional[bool] = None

class Car(CarBase):
    id: int
    images: List[CarImage] = []
    
    class Config:
        from_attributes = True
