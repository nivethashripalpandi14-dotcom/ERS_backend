

from pydantic import BaseModel, EmailStr
from app.models.Bookings import BookingStatus


class UserBookingCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    concerttable_id: int
    booking_status: BookingStatus = BookingStatus.Booked