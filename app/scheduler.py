from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone
from sqlalchemy import delete

from database import async_session_maker
from models import ShortURL


async def delete_expired():
    async with async_session_maker() as session:
        try:
            await session.execute(
                delete(ShortURL).where(
                    ShortURL.expires_at < datetime.now(timezone.utc)
                )
            )
            await session.commit()
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка при очистке URL: {e}")
            await session.rollback()


def init_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        delete_expired,
        'interval',
        minutes=5,
        next_run_time=datetime.now(timezone.utc),
        id='url_cleanup',
        replace_existing=True
    )

    return scheduler
