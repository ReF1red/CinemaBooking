from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from fastapi import HTTPException, status

class CityService:
    @staticmethod
    def get_all_cities(db: Session):
        return db.query(models.City).all()

    @staticmethod
    def get_city_by_id(db: Session, city_id: int):
        city = db.query(models.City).filter(models.City.city_id == city_id).first()
        if city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found"
            )
        return city

    @staticmethod
    def create_city(db: Session, city_data: schemas.CityCreate):
        exist_city = db.query(models.City).filter(models.City.city_name == city_data.city_name).first()
        if exist_city:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="City already exists"
            )
        
        new_city = models.City(city_name=city_data.city_name)
        db.add(new_city)
        db.commit()
        db.refresh(new_city)
        return new_city

    @staticmethod
    def update_city(db: Session, city_id: int, city_data: schemas.CityCreate):
        city = CityService.get_city_by_id(db, city_id)
        
        city.city_name = city_data.city_name
        
        db.commit()
        db.refresh(city)
        
        return city
    
    @staticmethod
    def delete_city(db: Session, city_id: int):
        city = CityService.get_city_by_id(db, city_id)
        cinemas = db.query(models.Cinema).filter(models.Cinema.city_id == city_id).all()
        if cinemas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't delete a city with cinemas."
            )
        
        db.delete(city)
        db.commit()
        return {"message": "City is deleted"}