


from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from app.database.database import AsyncSessionLocal


# ===================================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()




