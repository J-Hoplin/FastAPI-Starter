from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from apps.api.user.controller import user_router
from apps.core.lifespan import application_lifespan
from apps.api.health import health_check_router
from apps.application_docs import document_router
from apps.containers import root_container

load_dotenv()

# Disable docs_url and lock swagger ui (/swagger)
app = FastAPI(
    title="Hoplin FastAPI Template",
    description="Hoplin FastAPI Template",
    version="0.0.1",
    lifespan=application_lifespan,
    docs_url=None,
    openapi_url="/docs/openapi.json",
)

# Global Dependency Injection
root_container.wire(
    packages=[
        "apps.api",
        "apps.worker",
    ],
)

# CORS Setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Application Entry Route
api_entry = APIRouter(prefix="/api")

# API Router
api_entry.include_router(health_check_router)


# Global Application Router
app.include_router(document_router)
app.include_router(user_router)
app.include_router(api_entry)
