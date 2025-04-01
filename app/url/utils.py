import base62
import hashlib
import sys
from fastapi import HTTPException
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

sys.path.append(
    str(Path(__file__).parent.parent.parent)
)
from app.url.schemas import URLCreate, URLUpdate
from app.models import ShortURL


def generate_short_url(url: str) -> str:
    # original_url = str(url)
    hash = hashlib.sha256(url.encode()).hexdigest()
    numeric_hash = int(hash, 16) % (10**8)
    short_url = base62.encode(numeric_hash)
    return short_url


async def create_short_url(
    db: AsyncSession, url_data: URLCreate, user_id: int = None
):
    url = str(url_data.original_url)

    existing_url = await db.execute(
        select(ShortURL).filter(ShortURL.original_url == url)
    )
    if existing_url.scalars().first():
        raise HTTPException(
            status_code=400, detail='This URL already has short link!'
        )

    if url_data.custom_alias:
        short_url = url_data.custom_alias
    else:
        short_url = generate_short_url(url)

    db_url = ShortURL(
        original_url=url,
        short_code=short_url,
        expires_at=url_data.expires_at.astimezone(
            timezone.utc
        ) if url_data.expires_at else None,
        owner_id=user_id
    )
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url


async def update_url(
    db: AsyncSession, short_code: str, url_data: URLUpdate
    # user_id: int
):
    new_original_url = url_data.new_original_url
    new_alias = url_data.new_url
    new_expiry = url_data.expires_at

    result = await db.execute(
        select(ShortURL).filter(ShortURL.short_code == short_code)
    )
    url = result.scalars().first()

    # if not url or url.owner_id != user_id:
    #     raise HTTPException(status_code=400, detail='Permission denied')
    if not url:
        raise HTTPException(
            status_code=400, detail='No data with this short link'
        )
    elif new_original_url and new_alias:
        raise HTTPException(
            status_code=400,
            detail='You can not change both URL and short link'
        )
    else:
        if new_original_url:
            url.original_url = new_original_url
        if new_alias:
            url.short_code = new_alias
        if new_expiry:
            url.expires_at = new_expiry

    url.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(url)
    return url


async def get_original_url(db: AsyncSession, short_code: str):
    result = await db.execute(
        select(ShortURL).filter(ShortURL.short_code == short_code)
    )
    url = result.scalars().first()
    visit_count = url.visit_count
    visit_count += 1
    url.visit_count = visit_count
    url.last_accessed = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(url)

    return url


async def delete_url(db: AsyncSession, short_code: str):
    url = await get_original_url(db, short_code)
    # if url and url.owner_id == user_id:
    if not url:
        raise HTTPException(status_code=400, detail='No data')
    await db.delete(url)
    await db.commit()
    return True


async def get_url_stats(db: AsyncSession, short_code: str):
    result = await db.execute(
        select(ShortURL).where(ShortURL.short_code == short_code)
    )
    url = result.scalars().first()
    if not url:
        raise HTTPException(status_code=404, detail='Not Found')
    return url


async def get_url_by_origin(db: AsyncSession, original_url: str):
    result = await db.execute(
        select(ShortURL).where(ShortURL.original_url == original_url)
    )
    url = result.scalars().first()
    if not url:
        raise HTTPException(status_code=404, detail='Not Found')
    return url
