# src/tracker/composition.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.applications.adapters.outbound.sql_application_repository import SqlApplicationRepository
from tracker.applications.application.change_status import ChangeApplicationStatus
from tracker.applications.application.create_application import CreateApplication
from tracker.applications.application.list_applications import ListApplications
from tracker.applications.application.ports import ApplicationRepository
from tracker.shared.database import get_async_db


def get_application_repository(
    session: AsyncSession = Depends(get_async_db),
) -> ApplicationRepository:
    return SqlApplicationRepository(session)


def get_create_application(
    repo: ApplicationRepository = Depends(get_application_repository),
) -> CreateApplication:
    return CreateApplication(repo)


def get_list_applications(
    repo: ApplicationRepository = Depends(get_application_repository),
) -> ListApplications:
    return ListApplications(repo)


def get_change_status(
    repo: ApplicationRepository = Depends(get_application_repository),
) -> ChangeApplicationStatus:
    return ChangeApplicationStatus(repo)