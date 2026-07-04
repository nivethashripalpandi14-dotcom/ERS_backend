from pydantic import BaseModel,ConfigDict
from datetime import date, datetime



# Create Payment
class PaymentCreate(BaseModel):
    bookingtable_id: int
    amount: float
    payment_method: str
    transaction_id: str



# Read Payment
class PaymentRead(BaseModel):
    id: int
    bookingtable_id: int
    amount: float
    payment_method: str
    transaction_id: str | None = None
    payment_date: datetime
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_atributes=True)


# Update Payment
class PaymentUpdate(BaseModel):
    amount: float | None = None
    payment_method: str | None = None
    transaction_id: str | None = None


# Delete Payment
class PaymentDelete(BaseModel):
    id: int