from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    price_per_day = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    features = Column(JSON, nullable=True) # List of strings
    specs = Column(JSON, nullable=True)    # Key-value pairs (Engine, Transmission, etc.)
    primary_image_url = Column(String, nullable=True)

    images = relationship("CarImage", back_populates="car", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="car")

class CarImage(Base):
    __tablename__ = "car_images"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    image_url = Column(String, nullable=False)

    car = relationship("Car", back_populates="images")
