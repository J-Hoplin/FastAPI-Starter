from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager


"""
FastAPI Lifespan Documentation

https://fastapi.tiangolo.com/advanced/events/#lifespan

- Application Startup
- Application Terminate
"""


async def on_application_start(app:FastAPI):
    logger.info("Application Start")


async def on_application_stop(app:FastAPI):
    logger.info("Application Stop")


@asynccontextmanager
async def application_lifespan(app:FastAPI):
    await on_application_start(app)
    yield
    await on_application_stop(app)
