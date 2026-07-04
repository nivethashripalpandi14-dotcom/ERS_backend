from pydantic import BaseModel, ConfigDict
from datetime import  date, datetime


# Create Concert
class ConcertCreate(BaseModel):
    concert_name: str
    artist_name: str
    venue: str
    concert_date: date
    total_seats: int
    ticket_price: float


# Read Concert
class ConcertRead(BaseModel):
    id: int
    concert_name: str
    artist_name: str
    venue: str
    concert_date: date
    total_seats: int
    ticket_price: float
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes= True)


# Update Concert
class ConcertUpdate(BaseModel):
    concert_name: str | None = None
    artist_name: str | None = None
    venue: str | None = None
    concert_date: date | None = None
    total_seats: int | None = None
    ticket_price: float | None = None



# Delete Concert
class ConcertDelete(BaseModel):
    id: int


