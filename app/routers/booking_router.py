from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.booking_schema import (
    BookingCreate,
    BookingRead,
    BookingUpdate
)
from app.services.booking_services import (
    create_booking_service,
    get_bookings_service,
    update_booking,
    delete_booking
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# # Create Booking
# @router.post("/", response_model=BookingRead)
# async def create_booking_api(
#     data: BookingCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     booking = await create_booking_service(data, db)
#     return booking


# # Get All Bookings
# @router.get("/", response_model=list[BookingRead])
# async def get_all_bookings_api(
#     id: int | None = Query(None),
#     db: AsyncSession = Depends(get_db)
# ):
#     bookings = await get_bookings_service(id, db)
#     return bookings


# # Update Booking
# @router.patch("/{id}", response_model=BookingRead)
# async def update_booking_api(
#     id: int,
#     booking: BookingUpdate,
#     db: AsyncSession = Depends(get_db)
# ):
#     updated_booking = await update_booking(id, booking, db)
#     return updated_booking


# # Delete Booking
# @router.delete("/{id}")
# async def delete_booking_api(
#     id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     deleted_booking = await delete_booking(id, db)
#     return deleted_booking