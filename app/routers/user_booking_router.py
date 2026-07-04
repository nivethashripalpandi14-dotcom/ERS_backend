

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.user_booking_schema import UserBookingCreate
from app.services.user_booking_service import (
    create_user_and_booking_service,
    get_all_user_bookings_service,
    send_ticket_service)
router = APIRouter(
    prefix="/user-booking",
    tags=["User Booking"]
)


@router.post("/")
async def create_user_and_booking(
    data: UserBookingCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_user_and_booking_service(data, db)

@router.get("/")
async def get_all_user_bookings(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_user_bookings_service(db)

@router.patch("/{booking_id}/send-ticket")
async def send_ticket(
    booking_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await send_ticket_service(
        booking_id,
        db
    )

@router.patch("/send-ticket/{booking_id}")
async def send_ticket(
    booking_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await send_ticket_service(booking_id, db)