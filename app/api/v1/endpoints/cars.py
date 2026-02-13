from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.car import Car, CarCreate, CarUpdate
from app.services import car as car_service
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Car])
def read_cars(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    # Public endpoint to list available cars
    return car_service.get_multi_available(db, skip=skip, limit=limit)

@router.get("/all", response_model=List[Car])
def read_all_cars(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    # Admin endpoint to list all cars (including unavailable)
    return car_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Car)
def create_car(
    *,
    db: Session = Depends(deps.get_db),
    car_in: CarCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    car = car_service.create_with_images(db, obj_in=car_in, images=car_in.images)
    return car

@router.get("/{id}", response_model=Car)
def read_car(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    car = car_service.get(db, id=id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.put("/{id}", response_model=Car)
def update_car(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    car_in: CarUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    car = car_service.get(db, id=id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car = car_service.update(db, db_obj=car, obj_in=car_in)
    return car

@router.delete("/{id}", response_model=Car)
def delete_car(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    car = car_service.get(db, id=id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    car = car_service.remove(db, id=id)
    return car
