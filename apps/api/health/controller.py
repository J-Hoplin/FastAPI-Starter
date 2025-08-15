from fastapi import APIRouter
from fastapi.params import Depends

import sqlalchemy
from apps.api.health.serializers import HealthCheckResponse
from dependency_injector.wiring import Provide, inject
from apps.containers import Application
from apps.core.database.db import Database

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
    response_model=HealthCheckResponse,
)
@inject
async def health_check(
    db: Database = Depends(Provide[Application.db])
) -> HealthCheckResponse:
    database_ping = False
    async with db.session() as session:
        test_query = await session.execute(sqlalchemy.text("SELECT 1"))
        database_ping = test_query.scalar()

    return HealthCheckResponse(
        **{
            "status": "OK",
            "database_status": "OK" if bool(database_ping) else "Disconnected",
        }
    )
