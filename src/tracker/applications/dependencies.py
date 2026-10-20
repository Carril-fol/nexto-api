from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.shared.database import get_async_db
from tracker.applications.repository import ApplicationsRepository
from tracker.applications.service import ApplicationsService

def get_applications_repo(db: AsyncSession = Depends(get_async_db, scope="function")):
    return ApplicationsRepository(db)

def get_applications_service(repo: ApplicationsRepository = Depends(get_applications_repo)):
    return ApplicationsService(repo)