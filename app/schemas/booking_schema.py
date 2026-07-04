from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

from app.models.Bookings import BookingStatus


# Create Booking
class BookingCreate(BaseModel):
    usertable_id: int
    concerttable_id: int
    booking_status: BookingStatus = BookingStatus.Booked


# Read Booking
class BookingRead(BaseModel):
    id: int
    usertable_id: int
    concerttable_id: int
    booking_status: BookingStatus
    booking_date: datetime
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_atributes=True)

# Update Booking
class BookingUpdate(BaseModel):
    booking_status: BookingStatus | None = None

    # Delete Booking
class BookingDelete(BaseModel):
    id: int