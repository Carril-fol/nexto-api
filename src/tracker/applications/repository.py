from sqlalchemy.ext.asyncio import AsyncSession

from tracker.shared.base.repository import BaseRepository
from tracker.applications.models import Application


class ApplicationsRepository(BaseRepository[Application]):

    def __init__(self, db: AsyncSession):
        super().__init__(Application, db)