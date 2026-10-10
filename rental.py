from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    rent_days = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rentals")
    car = relationship("Car", back_populates="rentals")