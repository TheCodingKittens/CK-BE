from app.api.api_v1.customer import router as customer_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(customer_router, prefix="/customer", tags=["customer"])

