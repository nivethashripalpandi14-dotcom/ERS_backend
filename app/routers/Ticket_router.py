from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.Ticket_services import send_ticket_service

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/{booking_id}")
async def send_ticket(
    booking_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    return await send_ticket_service(
        booking_id,
        db,
        background_tasks
    )