# applications/application/list_applications.py
from tracker.applications.domain.entities import JobApplication

from .ports import ApplicationRepository


class ListApplications:
    def __init__(self, repo: ApplicationRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[JobApplication]:
        return await self._repo.list_all()