from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.Payments import Payments
from app.models.Bookings import Bookings
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate


# Create Payment
async def create_payment_service(
    data: PaymentCreate,
    db: AsyncSession,
):
    # Check booking exists
    result = await db.execute(
        select(Bookings).where(Bookings.id == data.bookingtable_id)
    )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Check transaction_id uniqueness
    result = await db.execute(
        select(Payments).where(
            Payments.transaction_id == data.transaction_id
        )
    )
    result = result.scalar_one_or_none()

    if result:
        raise HTTPException(
            status_code=400,
            detail="Transaction ID already exists"
        )

    # Check whether payment already exists for this booking
    result = await db.execute(
        select(Payments).where(
            Payments.bookingtable_id == data.bookingtable_id
        )
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Payment already exists for this booking"
        )

    db_payment = Payments(
        bookingtable_id=data.bookingtable_id,
        amount=data.amount,
        payment_method=data.payment_method,
        transaction_id=data.transaction_id,
    )

    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)

    return db_payment


# Get Payments
async def get_payments_service(
    id: int | None,
    db: AsyncSession,
):
    # Get a particular payment
    if id is not None:
        result = await db.execute(
            select(Payments).where(Payments.id == id)
        )
        payment = result.scalar_one_or_none()

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return [payment]

    # Get all payments
    result = await db.execute(select(Payments))
    payments = result.scalars().all()

    return payments


# Update Payment
async def update_payment(
    id: int,
    payment: PaymentUpdate,
    db: AsyncSession,
):
    result = await db.execute(
        select(Payments).where(Payments.id == id)
    )
    db_payment = result.scalar_one_or_none()

    if not db_payment:
        return None

    update_data = payment.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided to update"
        )

    # Check transaction_id uniqueness
    if "transaction_id" in update_data:
        result = await db.execute(
            select(Payments).where(
                Payments.transaction_id == update_data["transaction_id"],
                Payments.id != id
            )
        )
        existing_transaction = result.scalar_one_or_none()

        if existing_transaction:
            raise HTTPException(
                status_code=400,
                detail="Transaction ID already exists"
            )

    for key, value in update_data.items():
        setattr(db_payment, key, value)

    await db.commit()
    await db.refresh(db_payment)

    return db_payment


# Delete Payment
async def delete_payment(
    id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(Payments).where(Payments.id == id)
    )
    db_payment = result.scalar_one_or_none()

    if not db_payment:
        return None

    await db.delete(db_payment)
    await db.commit()

    return {"message": "Payment deleted successfully"}