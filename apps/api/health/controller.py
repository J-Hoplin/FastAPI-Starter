from fastapi import APIRouter
from apps.api.health.serializers import HealthCheckResponse

"""
Health Check Router

For container health check endpoint
"""

health_check_router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@health_check_router.get(
    path="/",
    summary="Health Check Route",
    description="Health Check Route",
    response_model=HealthCheckResponse
)
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(**{
        "status": "OK"
    })
