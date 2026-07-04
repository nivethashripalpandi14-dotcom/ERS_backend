from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, Enum as SqlEnum
from app.database.database import Base
from sqlalchemy.orm import relationship
from enum import Enum



class BookingStatus(str, Enum):
    Booked = "Booked"
    Ticket_Sent = "Ticket Sent"
    


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usertable_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    concerttable_id = Column(Integer, ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False)

    booking_status = Column(SqlEnum(BookingStatus),  default=BookingStatus.Booked)
    booking_date = Column(DateTime, server_default=func.now())

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("Users", back_populates="booking")
    concert = relationship("Concerts", back_populates="booking")
    payment = relationship("Payments", back_populates="booking", uselist=False, cascade="all, delete-orphan")


