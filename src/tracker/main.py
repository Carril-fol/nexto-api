# src/tracker/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from tracker.applications.adapters.inbound.http import router as applications_router
from tracker.applications.adapters.outbound.models import Base
from tracker.shared.database import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   # solo desarrollo; luego Alembic
    yield
    await engine.dispose()


app = FastAPI(title="Job Application Tracker", lifespan=lifespan)
app.include_router(applications_router)

