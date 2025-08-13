from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    database_status: str
