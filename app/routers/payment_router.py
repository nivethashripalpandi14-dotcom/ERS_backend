from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.schemas.payment_schema import (
    PaymentCreate,
    PaymentRead,
    PaymentUpdate
)
from app.services.payment_services import (
    create_payment_service,
    get_payments_service,
    update_payment,
    delete_payment
)

router = APIRouter(prefix="/payments", tags=["Payments"])


# Create Payment
@router.post("/", response_model=PaymentRead)
async def create_payment_api(
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db)
):
    payment = await create_payment_service(data, db)
    return payment


# # Get All Payments
# @router.get("/", response_model=list[PaymentRead])
# async def get_all_payments_api(
#     id: int | None = Query(None),
#     db: AsyncSession = Depends(get_db)
# ):
#     payments = await get_payments_service(id, db)
#     return payments


# # Update Payment
# @router.patch("/{id}", response_model=PaymentRead)
# async def update_payment_api(
#     id: int,
#     payment: PaymentUpdate,
#     db: AsyncSession = Depends(get_db)
# ):
#     updated_payment = await update_payment(id, payment, db)
#     return updated_payment


# # Delete Payment
# @router.delete("/{id}")
# async def delete_payment_api(
#     id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     deleted_payment = await delete_payment(id, db)
#     return deleted_payment