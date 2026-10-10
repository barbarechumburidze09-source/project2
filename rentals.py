from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_current_user, require_role

from app.core.database import get_db
from app.models.car import Car
from app.models.rental import Rental
from app.models.user import User
from app.schemas.rental import RentRequest, RentalResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/Rentals", tags=["Rentals"])

@router.post("/cars/{car_id}/rent", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
async def rent_car(
    car_id: int,
    rent_days: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    car = await db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="მანქანა ვერ მოიძებნა")
    
    if car.is_available is False:
        raise HTTPException(status_code=400, detail="მანქანა უკვე დაკავებულია")

    total = car.price_per_day * rent_days
    rental = Rental(
        user_id=current_user.id,
        car_id=car_id,
        rent_days=rent_days,
        total_price=total,
        city=car.city
    )
    
    car.is_available = False

    db.add(rental)
    await db.commit()
    await db.refresh(rental)
    return rental

@router.get("/", response_model=list[RentalResponse])
async def get_all_rentals(
    db: AsyncSession = Depends(get_db),
    
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Rental))
    return result.scalars().all()
from sqlalchemy.orm import joinedload

@router.get("/all-with-details")
async def get_all_rentals_with_details(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Rental).options(
        joinedload(Rental.user),
        joinedload(Rental.car)
    )
    result = await db.execute(stmt)
    return result.scalars().all()