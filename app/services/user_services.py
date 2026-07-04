from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.users import Users
from app.schemas.user_schema import UserCreate, UserUpdate, UserProfileUpdate
from app.models.Bookings import Bookings, BookingStatus
from app.models.Payments import Payments


# Create User
async def create_user_service(
    data: UserCreate,
    db: AsyncSession, 
):
    result = await db.execute(select(Users).where(Users.email == data.email))
    result = result.scalar_one_or_none()

    if result:
        raise HTTPException(status_code=400, detail="Email already registered")

    if data.phone_number:
        result = await db.execute(select(Users).where(Users.phone_number == data.phone_number))

        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Phone number already registered")        

    db_user = Users(
        username=data.username,
        email=data.email,
        phone_number=data.phone_number,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user



async def get_users_service(
    id: int | None,
    db: AsyncSession,
):
    # Get a particular user
    if id is not None:
        result = await db.execute(select(Users).where(Users.id == id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return [user]

    # Get all users
    result = await db.execute(select(Users))
    users = result.scalars().all()

    return users




async def get_user_ticket_service(
    id: int | None,
    email: str | None,
    db: AsyncSession,
):
    result = (
        select(Users)
        .options(
            selectinload(Users.booking).selectinload(Bookings.concert),
            selectinload(Users.booking).selectinload(Bookings.payment)
        )
    )

    if id is not None:
        result = result.where(Users.id == id)

    if email is not None:
        result = result.where(Users.email == email)

    result = await db.execute(result)
    users = result.scalars().all()

    if (id is not None or email is not None) and not users:
        raise HTTPException(status_code=404, detail="User not found")

    return [
        {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,

            "bookings": [
                {
                    "booking_id": booking.id,
                    "booking_status": booking.booking_status,

                    "concert": {
                        "concert_id": booking.concert.id,
                        "concert_name": booking.concert.concert_name,
                        "artist_name": booking.concert.artist_name,
                        "venue": booking.concert.venue,
                        "concert_date": booking.concert.concert_date,
                        "ticket_price": booking.concert.ticket_price
                    },

                    "payment": (
                        {
                            "payment_id": booking.payment.id,
                            "amount": booking.payment.amount,
                            "payment_method": booking.payment.payment_method,
                            "transaction_id": booking.payment.transaction_id,
                            "payment_date": booking.payment.payment_date
                        }
                        if booking.payment
                        else None
                    )
                }
                for booking in user.booking
            ]
        }
        for user in users
    ]







# Update User
async def update_user(
    id: int, 
    user: UserUpdate,
    db: AsyncSession, 
):
    result = await db.execute(select(Users).where(Users.id == id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    # Check email uniqueness
    if "email" in update_data:
        result = await db.execute(select(Users).where(Users.email == update_data["email"], Users.id != id))
        existing_email = result.scalar_one_or_none()

        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

    # Check phone number uniqueness
    if "phone_number" in update_data:
        result = await db.execute(select(Users).where(Users.phone_number == update_data["phone_number"], Users.id != id))
        existing_phone = result.scalar_one_or_none()

        if existing_phone:
            raise HTTPException(status_code=400, detail="Phone number already exists")

    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)

    return db_user



async def update_profile_service(
    email: str,
    data: UserProfileUpdate,
    db: AsyncSession
):
    # Get User
    user = await db.execute(
        select(Users)
        .where(
            Users.email == email,
            Users.deleted_at.is_(None)       
        )
    )
    db_user = user.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 2. Get latest booking (you can adjust logic if needed)
    result = await db.execute(
        select(Bookings)
        .where(Bookings.usertable_id == db_user.id)
        .order_by(Bookings.id.desc())
    )
    booking = result.scalar_one_or_none()

    # 3. BLOCK UPDATE if ticket already sent
    if booking and booking.booking_status == BookingStatus.Ticket_Sent:
        raise HTTPException(
            status_code=403,
            detail="Cannot update profile after ticket has been sent"
        )

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    # 4. EMAIL uniqueness check
    if "email" in update_data:
        result = await db.execute(
            select(Users).where(
                Users.email == update_data["email"],
                Users.id != db_user.id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists")

    # 5. PHONE uniqueness check
    if "phone_number" in update_data:
        result = await db.execute(
            select(Users).where(
                Users.phone_number == update_data["phone_number"],
                Users.id != db_user.id
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Phone number already exists")

    # 6. Update USER fields
    user_fields = ["username", "email", "phone_number"]
    for field in user_fields:
        if field in update_data:
            setattr(db_user, field, update_data[field])

    # 7. Update PAYMENT (latest booking payment)
    payment_fields = ["amount", "payment_method", "transaction_id"]

    if booking:
        result = await db.execute(
            select(Payments).where(Payments.bookingtable_id == booking.id)
        )
        payment = result.scalar_one_or_none()

        if payment:
            for field in payment_fields:
                if field in update_data:
                    setattr(payment, field, update_data[field])

    await db.commit()
    await db.refresh(db_user)

    return db_user






# Delete User
async def delete_user(
    id: int,
    db: AsyncSession, 
):
    result = await db.execute(select(Users).where(Users.id == id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()

    return {"message": "User deleted successfully"}