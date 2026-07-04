
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.Bookings import Bookings
from app.models.users import Users
from app.models.concerts import Concerts
from app.schemas.booking_schema import BookingCreate, BookingUpdate


# Create Booking
async def create_booking_service(
    data: BookingCreate,
    db: AsyncSession,
):
    # Check user exists
    result = await db.execute(
        select(Users).where(Users.id == data.usertable_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

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

    # Prevent duplicate booking
    result = await db.execute(
        select(Bookings).where(
            Bookings.usertable_id == data.usertable_id,
            Bookings.concerttable_id == data.concerttable_id
        )
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="User has already booked this concert"
        )

    db_booking = Bookings(
        usertable_id=data.usertable_id,
        concerttable_id=data.concerttable_id,
        booking_status=data.booking_status
    )

    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)

    return db_booking


# Get Booking(s)
async def get_bookings_service(
    id: int | None,
    db: AsyncSession,
):
    if id is not None:
        result = await db.execute(
            select(Bookings).where(Bookings.id == id)
        )

        booking = result.scalar_one_or_none()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return [booking]

    result = await db.execute(select(Bookings))
    bookings = result.scalars().all()

    return bookings


# Update Booking
async def update_booking(
    id: int,
    booking: BookingUpdate,
    db: AsyncSession,
):
    result = await db.execute(
        select(Bookings).where(Bookings.id == id)
    )

    db_booking = result.scalar_one_or_none()

    if not db_booking:
        return None

    update_data = booking.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided to update"
        )

    # Validate usertable_id if passed
    if "usertable_id" in update_data:
        result = await db.execute(
            select(Users).where(
                Users.id == update_data["usertable_id"]
            )
        )

        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    # Validate concerttable_id if passed
    if "concerttable_id" in update_data:
        result = await db.execute(
            select(Concerts).where(
                Concerts.id == update_data["concerttable_id"]
            )
        )

        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=404,
                detail="Concert not found"
            )

    # Prevent duplicate booking during update
    new_user_id = update_data.get(
        "usertable_id",
        db_booking.usertable_id
    )

    new_concert_id = update_data.get(
        "concerttable_id",
        db_booking.concerttable_id
    )

    result = await db.execute(
        select(Bookings).where(
            Bookings.usertable_id == new_user_id,
            Bookings.concerttable_id == new_concert_id,
            Bookings.id != id
        )
    )

    duplicate_booking = result.scalar_one_or_none()

    if duplicate_booking:
        raise HTTPException(
            status_code=400,
            detail="User has already booked this concert"
        )

    for key, value in update_data.items():
        setattr(db_booking, key, value)

    await db.commit()
    await db.refresh(db_booking)

    return db_booking


# Delete Booking
async def delete_booking(
    id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(Bookings).where(Bookings.id == id)
    )

    db_booking = result.scalar_one_or_none()

    if not db_booking:
        return None

    await db.delete(db_booking)
    await db.commit()

    return {
        "message": "Booking deleted successfully"
    }

