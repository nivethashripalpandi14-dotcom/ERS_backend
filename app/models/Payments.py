from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Enum
from app.database.database import Base
from sqlalchemy.orm import relationship








class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bookingtable_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)

    amount = Column(Float, nullable=False)
    payment_method = Column( String(50),nullable=False )  
    transaction_id = Column(String(255), unique=True, nullable=True)
    payment_date = Column(DateTime, server_default=func.now())

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    booking = relationship("Bookings", back_populates="payment")