from fastapi import APIRouter
from app.api.v1.endpoints import login, users, cars, bookings, content, register

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(register.router, tags=["register"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cars.router, prefix="/cars", tags=["cars"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
