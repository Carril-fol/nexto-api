# src/tracker/shared/db.py
import re
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from tracker.shared.config import settings

engine = create_async_engine(
    re.sub(r"^postgresql:", "postgresql+psycopg:", settings.database_url),
    echo=settings.db_echo,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise