from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.concert_schema import (
    ConcertCreate,
    ConcertRead,
    ConcertUpdate
)
from app.services.concert_services import (
    create_concert_service,
    get_concerts_service, get_concert_booking_service,
    update_concert,
    delete_concert
)

router = APIRouter(
    prefix="/concerts",
    tags=["Concerts"]
)


# Create Concert
@router.post("/", response_model=ConcertRead)
async def create_concert_api(
    data: ConcertCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_concert_service(data, db)


# Get Concert(s)
@router.get("/", response_model=list[ConcertRead])
async def get_concerts_api(
    id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    return await get_concerts_service(id, db)




# Get Concert(s)
@router.get("/detail/{id}")
async def get_concerts_api(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_concert_booking_service(id, db)









# Update Concert
@router.patch("/{id}", response_model=ConcertRead)
async def update_concert_api(
    id: int,
    concert: ConcertUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_concert = await update_concert(id, concert, db)
    return updated_concert


# Delete Concert
@router.delete("/{id}")
async def delete_concert_api(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted_concert = await delete_concert(id, db)
    return deleted_concert
