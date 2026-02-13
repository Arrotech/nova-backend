from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import models, schemas, services
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Booking])
def read_bookings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve all bookings (Admin only).
    """
    bookings = services.booking.get_multi(db, skip=skip, limit=limit)
    return bookings

@router.get("/me", response_model=List[schemas.Booking])
def read_my_bookings(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve bookings for the current user.
    """
    # Custom query because generic service doesn't support filtering by user_id yet
    return db.query(models.Booking).options(joinedload(models.Booking.car)).filter(models.Booking.user_id == current_user.id).all()

@router.post("/", response_model=schemas.Booking)
def create_booking(
    *,
    db: Session = Depends(deps.get_db),
    booking_in: schemas.BookingCreate,
    current_user: models.User = Depends(deps.get_current_active_user), # Require login for booking now
) -> Any:
    """
    Create new booking.
    """
    # Create booking with user linkage
    booking_data = booking_in.dict()
    booking = models.Booking(**booking_data, user_id=current_user.id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.put("/{booking_id}", response_model=schemas.Booking)
def update_booking(
    *,
    db: Session = Depends(deps.get_db),
    booking_id: int,
    booking_in: schemas.BookingUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a booking (Admin only).
    """
    booking = services.booking.get(db, id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking = services.booking.update(db, db_obj=booking, obj_in=booking_in)
    return booking
