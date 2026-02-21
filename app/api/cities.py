from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.database import get_db
from app.services.city_service import CityService
from app.api.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/cities", tags=["Cities and Cinemas"])

@router.get("/", response_model=List[schemas.CityOut])
def get_cities(
    db = Depends(get_db)
    ):
    return CityService.get_all_cities(db)

@router.get("/{city_id}/cinemas", response_model=List[schemas.CinemaOut])
def get_cinemas_by_city(
    city_id: int,
    db = Depends(get_db)
    ):
    return CityService.get_cinemas_by_city(db, city_id)

@router.post("/admin/cities", response_model=schemas.CityOut)
def create_city(
    city_data: schemas.CityCreate,
    db = Depends(get_db),
    current_user = Depends(get_current_admin)
    ):
    return CityService.create_city(db, city_data)

@router.delete("/admin/cities/{city_id}")
def delete_city(
    city_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_admin)
    ):
    return CityService.delete_city(db, city_id)

@router.post("/admin/cinemas", response_model=schemas.CinemaOut)
def create_cinema(
    cinema_data: schemas.CinemaCreate,
    db = Depends(get_db),
    current_user = Depends(get_current_admin)
    ):
    return CityService.create_cinema(db, cinema_data)

@router.delete("/admin/cinemas/{cinema_id}")
def delete_cinema(
    cinema_id: int,
    db = Depends(get_db),
    currnet_user = Depends(get_current_admin)
    ):
    return CityService.delete_cinema(db, cinema_id)