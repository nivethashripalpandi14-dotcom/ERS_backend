from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.concerts import Concerts
from app.schemas.concert_schema import ConcertCreate, ConcertUpdate
from app.models.Bookings import Bookings


# Create Concert
async def create_concert_service(
    data: ConcertCreate,
    db: AsyncSession,
):
    result = await db.execute(
        select(Concerts).where(
            Concerts.concert_name == data.concert_name,
            Concerts.artist_name == data.artist_name,
            Concerts.concert_date == data.concert_date
        )
    )
    result = result.scalar_one_or_none()

    if result:
        raise HTTPException(
            status_code=400,
            detail="Concert already exists"
        )

    db_concert = Concerts(
        concert_name=data.concert_name,
        artist_name=data.artist_name,
        venue=data.venue,
        concert_date=data.concert_date,
        total_seats=data.total_seats,
        ticket_price=data.ticket_price,
    )

    db.add(db_concert)
    await db.commit()
    await db.refresh(db_concert)

    return db_concert


# Get Concert(s)
async def get_concerts_service(
    id: int | None,
    db: AsyncSession,
):
    # Get a particular concert
    if id is not None:
        result = await db.execute(select(Concerts).where(Concerts.id == id))
        concert = result.scalar_one_or_none()

        if not concert:
            raise HTTPException(
                status_code=404,
                detail="Concert not found"
            )

        return [concert]

    # Get all concerts
    result = await db.execute(select(Concerts))
    concerts = result.scalars().all()

    return concerts



async def get_concert_booking_service(
    id: int,
    db: AsyncSession,
):
    query = (
        select(Concerts)
        .options(
            selectinload(Concerts.booking)
            .selectinload(Bookings.user),

            selectinload(Concerts.booking)
            .selectinload(Bookings.payment),
        )
        .where(Concerts.id == id)
    )

    result = await db.execute(query)
    concert = result.scalars().first()

    if not concert:
        raise HTTPException(status_code=404, detail="Concert not found")

    return {
        "concert_id": concert.id,
        "concert_name": concert.concert_name,
        "artist_name": concert.artist_name,
        "venue": concert.venue,
        "concert_date": concert.concert_date,
        "ticket_price": concert.ticket_price,

        "bookings": [
            {
                "booking_id": booking.id,
                "booking_status": booking.booking_status,

                "user": {
                    "user_id": booking.user.id,
                    "username": booking.user.username,
                    "email": booking.user.email,
                    "phone_number": booking.user.phone_number,
                },

                "payment": (
                    {
                        "payment_id": booking.payment.id,
                        "amount": booking.payment.amount,
                        "payment_method": booking.payment.payment_method,
                        "transaction_id": booking.payment.transaction_id,
                        "payment_date": booking.payment.payment_date,
                    }
                    if booking.payment
                    else None
                )
            }
            for booking in concert.booking
        ]
    }




# Update Concert
async def update_concert(
    id: int,
    concert: ConcertUpdate,
    db: AsyncSession,
):
    result = await db.execute(
        select(Concerts).where(Concerts.id == id)
    )
    db_concert = result.scalar_one_or_none()

    if not db_concert:
        return None

    update_data = concert.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided to update"
        )

    # Check duplicate concert
    if (
        "concert_name" in update_data
        or "artist_name" in update_data
        or "concert_date" in update_data
    ):
        concert_name = update_data.get(
            "concert_name",
            db_concert.concert_name
        )
        artist_name = update_data.get(
            "artist_name",
            db_concert.artist_name
        )
        concert_date = update_data.get(
            "concert_date",
            db_concert.concert_date
        )

        result = await db.execute(
            select(Concerts).where(
                Concerts.concert_name == concert_name,
                Concerts.artist_name == artist_name,
                Concerts.concert_date == concert_date,
                Concerts.id != id
            )
        )
        existing_concert = result.scalar_one_or_none()

        if existing_concert:
            raise HTTPException(
                status_code=400,
                detail="Concert already exists"
            )

    for key, value in update_data.items():
        setattr(db_concert, key, value)

    await db.commit()
    await db.refresh(db_concert)

    return db_concert




# Delete Concert
async def delete_concert(
    id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(Concerts).where(Concerts.id == id)
    )
    db_concert = result.scalar_one_or_none()

    if not db_concert:
        return None

    await db.delete(db_concert)
    await db.commit()

    return {"message": "Concert deleted successfully"}