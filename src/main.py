from fastapi import FastAPI

from tracker.applications.router import router as applications_router
from tracker.users.router import router as users_router

app = FastAPI()
app.include_router(applications_router)
app.include_router(users_router)
