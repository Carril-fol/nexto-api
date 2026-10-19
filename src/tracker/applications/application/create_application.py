from uuid import UUID

from tracker.applications.domain.entities import JobApplication

from .ports import ApplicationRepository


class CreateApplication:
    def __init__(self, repo: ApplicationRepository) -> None:
        self._repo = repo

    async def execute(
        self, position: str, link: str, description: str, cv_id: UUID
    ) -> JobApplication:
        application = JobApplication.create(position, link, description, cv_id)
        await self._repo.add(application)
        return application