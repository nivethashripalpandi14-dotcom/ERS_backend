from fastapi import HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Bookings import Bookings
from app.Email_service import send_event_registration_email
from app.models.Bookings import BookingStatus


async def send_ticket_service(
    booking_id: int,
    db: AsyncSession,
    background_tasks: BackgroundTasks
):
    result = await db.execute(
        select(Bookings)
        .options(
            selectinload(Bookings.user),
            selectinload(Bookings.concert),
            selectinload(Bookings.payment)
        )
        .where(Bookings.id == booking_id)
    )

    booking = result.scalar_one_or_none()

    # Validation
    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    # Amount validation
    if booking.payment.amount != booking.concert.ticket_price:
        raise HTTPException(
            status_code=400,
            detail="Payment amount mismatch"
        )


    if booking.booking_status == BookingStatus.Ticket_Sent:
        raise HTTPException(status_code=400, detail="Ticket already sent")

    # Update status
    booking.booking_status = "Ticket_Sent"

    await db.commit()
    await db.refresh(booking)

    # Background email
    background_tasks.add_task(
        send_event_registration_email,
        booking.user.email,
        booking.concert.concert_name,
        booking.user.username,
        booking.concert.concert_date
    )

    return {
        "message": "Ticket sent successfully",
        "status": booking.booking_status
    }