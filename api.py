from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from apps.api.auth.controller import auth_router
from apps.api.user.controller import user_router
from apps.api.user.admin import UserAdmin
from apps.core.admin import AdminPageAuthentication
from apps.core.lifespan import application_lifespan
from apps.api.health import health_check_router
from apps.application_docs import document_router
from apps.containers import root_container
from apps.core.exception.base import root_exception_handler, RootException

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
    packages=["apps.api", "apps.worker", "apps.core.auth"],
)


# Admin Authentication & Admin Page: /admin
app.add_middleware(
    SessionMiddleware, secret_key=root_container.config.get("ADMIN_SESSION_SECRET_KEY")
)
admin = Admin(
    app=app,
    engine=root_container.db().engine,
    authentication_backend=AdminPageAuthentication(
        secret_key=root_container.config.get("ADMIN_SESSION_SECRET_KEY"),
        database=root_container.db(),
    ),
)
admin.add_view(UserAdmin)

# CORS Setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
app.add_exception_handler(RootException, root_exception_handler)

# API Application Entry Route
api_entry = APIRouter(prefix="/api")

# API Router
api_entry.include_router(health_check_router)
api_entry.include_router(user_router)
api_entry.include_router(auth_router)


# Global Application Router
app.include_router(document_router)
app.include_router(api_entry)
