# applications/application/change_status.py
from uuid import UUID

from tracker.applications.domain.entities import JobApplication
from tracker.applications.domain.errors import ApplicationNotFound

from .ports import ApplicationRepository


class ChangeApplicationStatus:
    def __init__(self, repo: ApplicationRepository) -> None:
        self._repo = repo

    async def execute(self, application_id: UUID, new_status: str) -> JobApplication:
        application = await self._repo.get(application_id)
        if application is None:
            raise ApplicationNotFound(application_id)

        application.change_status(new_status) 
        await self._repo.save(application)
        return application