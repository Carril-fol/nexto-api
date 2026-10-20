from fastapi import FastAPI

from tracker.applications.router import router as applications_router

app = FastAPI()
app.include_router(applications_router)

