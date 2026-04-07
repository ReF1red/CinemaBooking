from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from fastapi import HTTPException, status
from app.services.city_service import CityService

class CinemaService:
    @staticmethod
    def get_cinemas_by_city(db: Session, city_id: int):
        CityService.get_city_by_id(db, city_id)

        cinemas = db.query(models.Cinema).filter(models.Cinema.city_id == city_id).all()
        result = []
        for cinema in cinemas:
            result.append({
                "city_id": cinema.city_id,
                "city_name": cinema.city.city_name,
                "cinema_id": cinema.cinema_id,
                "cinema_name": cinema.cinema_name,
                "cinema_address": cinema.cinema_address
            })
        return result

    @staticmethod
    def get_cinema_by_id(db: Session, cinema_id: int):
        cinema = db.query(models.Cinema).filter(models.Cinema.cinema_id == cinema_id).first()
        if cinema is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cinema not found"
            )
        
        return {
            "city_id": cinema.city_id,
            "city_name": cinema.city.city_name,
            "cinema_id": cinema.cinema_id,
            "cinema_name": cinema.cinema_name,
            "cinema_address": cinema.cinema_address
        }

    @staticmethod
    def create_cinema(db: Session, cinema_data: schemas.CinemaCreate):
        city = CityService.get_city_by_id(db, cinema_data.city_id)
        
        new_cinema = models.Cinema(
            city_id=cinema_data.city_id,
            cinema_name=cinema_data.cinema_name,
            cinema_address=cinema_data.cinema_address
        )

        db.add(new_cinema)
        db.commit()
        db.refresh(new_cinema)
        return {
            "cinema_id": new_cinema.cinema_id,
            "city_id": new_cinema.city_id,
            "cinema_name": new_cinema.cinema_name,
            "cinema_address": new_cinema.cinema_address,
            "city_name": city.city_name
        }

    @staticmethod
    def update_cinema(db: Session, cinema_id: int, cinema_data: schemas.CinemaCreate):
        cinema = db.query(models.Cinema).filter(models.Cinema.cinema_id == cinema_id).first()
        city = db.query(models.City).filter(models.City.city_id == cinema_data.city_id).first()

        if not cinema:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Cinema not found"
            )
        
        if not city:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="City not found"
            )

        cinema.cinema_name = cinema_data.cinema_name
        cinema.cinema_address = cinema_data.cinema_address
        cinema.city_id = cinema_data.city_id
        
        db.commit()
        db.refresh(cinema)
        
        return {
            "cinema_id": cinema.cinema_id,
            "city_id": cinema.city_id,
            "cinema_name": cinema.cinema_name,
            "cinema_address": cinema.cinema_address,
            "city_name": city.city_name
        }

    @staticmethod
    def delete_cinema(db: Session, cinema_id: int):
        cinema = db.query(models.Cinema).filter(models.Cinema.cinema_id == cinema_id).first()

        if not cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cinema not found"
            )
        
        halls = db.query(models.Hall).filter(models.Hall.cinema_id == cinema_id).all()
        
        if halls:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't delete a cinema with halls."
            )
        
        db.delete(cinema)
        db.commit()
        return {"message": "Cinema is deleted"}