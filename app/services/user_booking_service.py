

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import Users
from app.models.Bookings import Bookings,BookingStatus
from app.models.concerts import Concerts
from app.schemas.user_booking_schema import UserBookingCreate
from app.Email_service import send_event_registration_email
async def create_user_and_booking_service(
    data: UserBookingCreate,
    db: AsyncSession,
):
    # Check email already exists
    result = await db.execute(
        select(Users).where(Users.email == data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    if data.phone_number:
        result = await db.execute(select(Users).where(Users.phone_number == data.phone_number))

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Phone number already registered")        


    # Check concert exists
    result = await db.execute(
        select(Concerts).where(Concerts.id == data.concerttable_id)
    )
    concert = result.scalar_one_or_none()

    if not concert:
        raise HTTPException(
            status_code=404,
            detail="Concert not found"
        )

    # Create user
    new_user = Users(
        username=data.username,
        email=data.email,
        phone_number=data.phone_number
    )

    db.add(new_user)
    await db.flush()   # gets generated user id

    # Create booking
    new_booking = Bookings(
        usertable_id=new_user.id,
        concerttable_id=data.concerttable_id,
        booking_status=data.booking_status
    )

    db.add(new_booking)

    await db.commit()
    await db.refresh(new_user)
    await db.refresh(new_booking)

    return {
        "message": "User and Booking created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "phone_number": new_user.phone_number
        },
        "booking": {
            "id": new_booking.id,
            "usertable_id": new_booking.usertable_id,
            "concerttable_id": new_booking.concerttable_id,
            "booking_status": new_booking.booking_status
        }
    }

from sqlalchemy import select
from app.models.Bookings import Bookings
from app.models.users import Users
from app.models.concerts import Concerts


async def get_all_user_bookings_service(db: AsyncSession):

    result = await db.execute(
        select(Bookings, Users, Concerts)
        .join(Users, Bookings.usertable_id == Users.id)
        .join(Concerts, Bookings.concerttable_id == Concerts.id)
    )

    records = result.all()

    bookings = []

    for booking, user, concert in records:

        bookings.append({
    "id": booking.id,
    "username": user.username,
    "email": user.email,
    "phone_number": user.phone_number,
    "concert_name": concert.concert_name,
    "booking_status": booking.booking_status
})

    return bookings

async def send_ticket_service(
    booking_id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(Bookings, Users, Concerts)
        .join(Users, Bookings.usertable_id == Users.id)
        .join(Concerts, Bookings.concerttable_id == Concerts.id)
        .where(Bookings.id == booking_id)
    )

    record = result.first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking, user, concert = record

    # if booking.booking_status == BookingStatus.Ticket_Sent:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Ticket already sent"
    #     )

    booking.booking_status = BookingStatus.Ticket_Sent
    await db.commit()

    await send_event_registration_email(
        email=user.email,
        username=user.username,
        concert_name=concert.concert_name,
        concert_date=str(concert.concert_date)
    )

    return {
        "message": "Ticket sent successfully"
    }

