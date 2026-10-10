from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base  

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price_per_day = Column(Float, nullable=False)

    image1_url = Column(String, nullable=True)
    image2_url = Column(String, nullable=True)
    image3_url = Column(String, nullable=True)

    capacity = Column(Integer, nullable=True, default=5)
    transmission = Column(String, nullable=True, default="Automatic")
    city = Column(String, nullable=True, default="Tbilisi")
    fuel_capacity = Column(Float, nullable=True)
    is_available = Column(Boolean, default=True, nullable=True)
    owner_phone = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="cars")

    
    rentals = relationship("Rental", back_populates="car", cascade="all, delete-orphan")

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)