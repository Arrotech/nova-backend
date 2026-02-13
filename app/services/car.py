from typing import List, Optional
from sqlalchemy.orm import Session
from app.services.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from app.models.car import Car, CarImage
from app.schemas.car import CarCreate, CarUpdate, CarImageCreate

class CRUDCar(CRUDBase[Car, CarCreate, CarUpdate]):
    def create_with_images(self, db: Session, *, obj_in: CarCreate, images: List[str]) -> Car:
        obj_in_data = jsonable_encoder(obj_in)
        if 'images' in obj_in_data:
            del obj_in_data['images']
            
        db_obj = Car(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        if images:
            for img_url in images:
                db_img = CarImage(car_id=db_obj.id, image_url=img_url)
                db.add(db_img)
            
            # Set primary image if available
            db_obj.primary_image_url = images[0]
            db.add(db_obj)
            
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

    def update(self, db: Session, *, db_obj: Car, obj_in: CarUpdate) -> Car:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        # Handle images separately
        images = update_data.pop('images', None)
        
        # Update standard fields
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Update images if provided
        if images is not None:
             # Delete existing images
            db.query(CarImage).filter(CarImage.car_id == db_obj.id).delete()
            
            # Add new images
            for img_url in images:
                db_img = CarImage(car_id=db_obj.id, image_url=img_url)
                db.add(db_img)
            
            # Update primary image if available
            if images:
                db_obj.primary_image_url = images[0]
                db.add(db_obj)
                
            db.commit()
            db.refresh(db_obj)
            
        return db_obj
    
    def get_multi_available(self, db: Session, skip: int = 0, limit: int = 100) -> List[Car]:
        return db.query(self.model).filter(self.model.is_available == True).offset(skip).limit(limit).all()

car = CRUDCar(Car)
