import shutil
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.dependencies import get_current_user, require_role

from app.core.database import get_db
from app.models.car import Car

router = APIRouter()

async def save_image(file: UploadFile) -> str:
    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = f"uploads/{unique_filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/uploads/{unique_filename}"


@router.get("/")
async def get_cars(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car))
    cars = result.scalars().all()
    return cars


@router.get("/{car_id}")
async def get_car(car_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="მანქანა ვერ მოიძებნა")
    return car


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_car(
    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    price_per_day: float = Form(...),
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    image3: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
 AsyncSession = Depends(get_db),
current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    img1_path = await save_image(image1)
    img2_path = await save_image(image2)
    img3_path = await save_image(image3)

    new_car = Car(
        brand=brand,
        model=model,
        year=year,
        price_per_day=price_per_day,
        image1_url=img1_path,
        image2_url=img2_path,
        image3_url=img3_path
    )

    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)

    return new_car

@router.put("/{car_id}")
async def update_car(
    car_id: int,
    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    price_per_day: float = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="მანქანა ვერ მოიძებნა")

    car.brand = brand
    car.model = model
    car.year = year
    car.price_per_day = price_per_day

    await db.commit()
    await db.refresh(car)
    return car


@router.patch("/{car_id}")
async def patch_car(
    car_id: int,
    brand: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    price_per_day: Optional[float] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="მანქანა ვერ მოიძებნა")

    if brand is not None:
        car.brand = brand
    if model is not None:
        car.model = model
    if year is not None:
        car.year = year
    if price_per_day is not None:
        car.price_per_day = price_per_day

    await db.commit()
    await db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    current_user: User = Depends(require_role([UserRole.ADMIN]))
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="მანქანა ვერ მოიძებნა")

    await db.delete(car)
    await db.commit()
    return None