from app.api.routes import books
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["books"])
