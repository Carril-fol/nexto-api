from tracker.applications.repository import ApplicationsRepository
from tracker.applications.schema import ApplicationCreate, ApplicationUpdate, ApplicationStatusUpdate
from tracker.applications.models import Application, ApplicationStatus
from tracker.applications.exceptions import ApplicationNotExists, ApplicationAlreadyHasThatStatus

class ApplicationsService:

    def __init__(self, application_repo: ApplicationsRepository):
        self.repo = application_repo

    async def _get_application_by_id_or_raise(self, id):
        application = await self.repo.get_by_id(id)
        if not application:
            raise ApplicationNotExists()
        return application

    async def create_job_application(self, data: ApplicationCreate):
        application = Application(**data.model_dump())
        await self.repo.create(application)

    async def update_job_application(self, id, data: dict):
        application = await self._get_application_by_id_or_raise(id)

        if application.status == ApplicationStatus.DELETED:
            raise ApplicationNotExists()

        update_fields = data.items()
        for field, value in update_fields:
            setattr(application, field, value)

        await self.repo.update(application)

    async def delete_job_application(self, id, data: dict):
        application = await self._get_application_by_id_or_raise(id)

        if application.status == ApplicationStatus.DELETED:
            raise ApplicationAlreadyHasThatStatus()

        update_fields = data.items()
        for field, value in update_fields:
            setattr(application, field, value)

        await self.repo.update(application)