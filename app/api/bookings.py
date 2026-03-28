from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.database import get_db
from app.services.booking_service import BookingService
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking_data: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return BookingService.create_booking(db, current_user.user_id, booking_data)

@router.get("/my", response_model=List[schemas.BookingOut])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return BookingService.get_user_bookings(db, current_user.user_id)

@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return BookingService.cancel_booking(db, booking_id, current_user.user_id)