from fastapi import APIRouter
from app.presentation.api.v1.endpoints import auth, categories, transactions, dashboard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(transactions.router)
api_router.include_router(dashboard.router)
