# applications/adapters/outbound/sql_repository.py
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.applications.domain.entities import JobApplication

from .models import ApplicationRow


class SqlApplicationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, application: JobApplication) -> None:
        self._session.add(self._to_row(application))
        await self._session.flush()

    async def get(self, application_id: UUID) -> JobApplication | None:
        row = await self._session.get(ApplicationRow, application_id)
        return self._to_entity(row) if row else None

    async def list_all(self) -> list[JobApplication]:
        stmt = select(ApplicationRow).order_by(ApplicationRow.created_at.desc())
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(r) for r in rows]

    async def save(self, application: JobApplication) -> None:
        await self._session.merge(self._to_row(application))
        await self._session.flush()

    @staticmethod
    def _to_row(a: JobApplication) -> ApplicationRow:
        return ApplicationRow(
            id=a.id, position=a.position, link=a.link,
            description=a.description, cv_id=a.cv_id,
            status=a.status, created_at=a.created_at,
        )

    @staticmethod
    def _to_entity(r: ApplicationRow) -> JobApplication:
        return JobApplication(
            id=r.id, position=r.position, link=r.link,
            description=r.description, cv_id=r.cv_id,
            status=r.status, created_at=r.created_at,
        )