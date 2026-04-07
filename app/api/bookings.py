from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.database import get_db
from app.services.booking_service import BookingService
from app.services.log_service import LogService
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking_data: schemas.BookingCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
    ):
    booking = BookingService.create_booking(db, current_user.user_id, booking_data)

    user_id = current_user.user_id if current_user else None
    user_email = current_user.email if current_user else None

    LogService.log_action(
        db = db,
        user_id = user_id,
        user_email = user_email,
        action_type = "CREATE_BOOKING",
        details = {
            "booking_id": booking["booking_id"],
            "session_id": booking["session_id"],
            "total_price": booking["total_price"],
            "seats_count": len(booking["seats"])
        },
        ip_address = request.client.host
    )

    return booking

@router.get("/my", response_model=List[schemas.BookingOut])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
    ):
    return BookingService.get_user_bookings(db, current_user.user_id)

@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
    ):
    booking = BookingService.get_booking_by_id(db, booking_id, current_user.user_id)


    user_id = current_user.user_id if current_user else None
    user_email = current_user.email if current_user else None

    LogService.log_action(
        db = db,
        user_id = user_id,
        user_email = user_email,
        action_type = "CANCEL_BOOKING",
        details = {"booking": {
            "booking_id": booking_id,
            "session_id": booking.session_id if booking else None,
            "total_price": booking.total_price if booking else None
        }},
        ip_address = request.client.host
    )

    return BookingService.cancel_booking(db, booking_id, current_user.user_id)