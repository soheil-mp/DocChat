from fastapi import APIRouter
from app.services.health_service import HealthService

router = APIRouter()
health_service = HealthService()

@router.get("/health")
async def health_check():
    return await health_service.check_services() 