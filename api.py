from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from apps.core.lifespan import application_lifespan
from apps.api.health import health_check_router
from apps.application_docs import document_router

load_dotenv()

# Disable docs_url and lock swagger ui (/swagger)
app = FastAPI(
    description="Hoplin FastAPI Template",
    version="0.0.1",
    lifespan=application_lifespan,
    docs_url=None,
    openapi_url="/docs/openapi.json",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "persistAuthorization": True
    }
)



# API Application Entry Route
api_entry = APIRouter(
    prefix="/api"
)

# API Router
api_entry.include_router(health_check_router)


# Global Application Router
app.include_router(document_router)
app.include_router(api_entry)