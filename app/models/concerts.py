from sqlalchemy import Column, Integer, String, DateTime, Float, Date, func
from app.database.database import Base
from sqlalchemy.orm import relationship


class Concerts(Base):
    __tablename__ = "concerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    concert_name = Column(String(255), nullable=False)
    artist_name = Column(String(255), nullable=False)
    venue = Column(String(255), nullable=False)
    concert_date = Column(Date, nullable=False)
    total_seats = Column(Integer, nullable=False)
    ticket_price = Column(Float, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    
    booking = relationship("Bookings", back_populates="concert", uselist=True, cascade="all, delete-orphan")


    