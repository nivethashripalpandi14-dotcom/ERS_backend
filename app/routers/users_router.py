from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.user_schema import UserUpdate
from app.schemas.user_schema import UserCreate, UserRead, UserProfileUpdate
from app.services.user_services import (
    create_user_service,get_user_ticket_service,
     update_user, update_profile_service,
    delete_user
)


router = APIRouter(prefix="/users", tags=["Users"])


# Create User
@router.post("/", response_model=UserRead)
async def create_user_api(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = await create_user_service(data, db)
    return user



@router.get("/")
async def get_user_ticket(
    id: int | None = None,
    email: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_ticket_service(id, email, db)
    return user


# Update User
@router.patch("/{id}", response_model=UserRead)
async def update_user_api(
    id: int,
    user: UserUpdate,

    db: AsyncSession = Depends(get_db)
):
    updated_user = await update_user(id, user, db)
    return updated_user




@router.patch("/profile/{email}")
async def update_profile(
    email: str,
    data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_user = await update_profile_service(
        email, data, db
    )
    return updated_user




# Delete User
@router.delete("/{id}")
async def delete_user_api(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted_user = await delete_user(id, db)
    return deleted_user