from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import date, datetime


# Create User
class UserCreate(BaseModel):
    username: str 
    email: EmailStr 
    phone_number: str


# Read User
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_atributes=True)


# Update User
class UserUpdate(BaseModel):
    username: str | None= None
    email: EmailStr | None = None
    phone_number: str | None = None


class UserProfileUpdate(BaseModel):
    username: str | None= None
    email: EmailStr | None = None
    phone_number: str | None = None
    amount: float | None = None
    payment_method: str | None = None
    transaction_id: str | None = None



    # Delete User
class UserDelete(BaseModel):
    id: int