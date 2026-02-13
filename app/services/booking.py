from typing import List
from sqlalchemy.orm import Session
from app.services.base import CRUDBase
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate, BookingBase

class CRUDBooking(CRUDBase[Booking, BookingCreate, BookingUpdate]):
    def get_by_customer_email(self, db: Session, email: str) -> List[Booking]:
        return db.query(self.model).filter(self.model.customer_email == email).all()

booking = CRUDBooking(Booking)
