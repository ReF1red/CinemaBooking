from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from fastapi import HTTPException

class CityService:
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
            raise HTTPException(status_code=404, detail="Cinema not found")
        
        return {
            "city_id": cinema.city_id,
            "city_name": cinema.city.city_name,
            "cinema_id": cinema.cinema_id,
            "cinema_name": cinema.cinema_name,
            "cinema_address": cinema.cinema_address
        }

    @staticmethod
    def create_cinema(db: Session, cinema_data: schemas.CinemaCreate):
        CityService.get_city_by_id(db, cinema_data.city_id)
        
        new_cinema = models.Cinema(
            city_id=cinema_data.city_id,
            cinema_name=cinema_data.cinema_name,
            cinema_address=cinema_data.cinema_address
        )

        db.add(new_cinema)
        db.commit()
        db.refresh(new_cinema)
        return new_cinema

    @staticmethod
    def update_cinema(db: Session, cinema_id: int, cinema_data: schemas.CinemaCreate):
        cinema = CityService.get_cinema_by_id(db, cinema_id)
        
        cinema.cinema_name = cinema_data.cinema_name
        cinema.cinema_address = cinema_data.cinema_address
        
        db.commit()
        db.refresh(cinema)
        
        return cinema

    @staticmethod
    def delete_cinema(db: Session, cinema_id: int):
        cinema = CityService.get_cinema_by_id(db, cinema_id)

        halls = db.query(models.Hall).filter(models.Hall.cinema_id == cinema_id).all()
        if halls:
            raise HTTPException(
                status_code=400,
                detail="You can't delete a cinema with halls."
            )
        
        db.delete(cinema)
        db.commit()
        return {"message": "Cinema is deleted"}