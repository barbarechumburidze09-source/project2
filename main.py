import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, cars, rentals
from app.core.database import engine, Base
import app.models  

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Car Rental API",
    description="Async API with FastAPI, PostgreSQL, and JWT",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "სერვერული შეცდომა: " + str(exc)},
    )

app.include_router(users.router, prefix="/api/Users", tags=["Users"])
app.include_router(cars.router, prefix="/api/Cars", tags=["Cars"])
app.include_router(rentals.router, prefix="/api/Rentals", tags=["Rentals"])