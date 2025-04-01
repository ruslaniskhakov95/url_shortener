import sys
from http import HTTPStatus
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
sys.path.append(
    str(Path(__file__).parent.parent.parent)
)
from app.database import get_async_session
from app.models import User
from app.url.schemas import (
    BaseURL, URLCreate, URLUpdate, URLResponse, URLStatsResponse,
    BaseShortURL
)
from app.url.utils import (
    create_short_url, get_original_url, delete_url, update_url,
    get_url_stats, get_url_by_origin
)
from app.user.router import fastapi_users


router = APIRouter(prefix='/links', tags=['links'])
current_active_user = fastapi_users.current_user(active=True)
security = HTTPBearer(auto_error=False)


@router.post(
    "/shorten", response_model=URLResponse, status_code=HTTPStatus.CREATED
)
async def shorten_url(
    data: URLCreate, session: AsyncSession = Depends(get_async_session),
    user: User = Depends(fastapi_users.current_user(active=True))
):
    short_url = await create_short_url(
        session, data, user.id if user else None
    )
    expires_at = data.expires_at

    return URLResponse(
        original_url=short_url.original_url, short_code=short_url.short_code,
        created_at=short_url.created_at, expires_at=expires_at,
        owner_id=user.id if user else None
    )


@router.get(
    "/search", response_model=BaseShortURL, status_code=HTTPStatus.OK
)
async def search_by_origin(
    original_url: str, session: AsyncSession = Depends(get_async_session)
):
    url = await get_url_by_origin(session, original_url)

    return BaseShortURL(
        short_code=url.short_code
    )


@router.get(
    "/{short_code}", response_model=BaseURL, status_code=HTTPStatus.OK
)
async def redirect_to_original_url(
    short_code: str, session: AsyncSession = Depends(get_async_session)
):
    url = await get_original_url(session, short_code)
    if not url:
        raise HTTPException(status_code=404, detail='Short URL not found')
    return BaseURL(original_url=url.original_url)


@router.put(
    "/{short_code}", response_model=URLResponse, status_code=HTTPStatus.OK
)
async def update_short_url(
    short_code: str, data: URLUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(fastapi_users.current_user(active=True))
):
    url = await get_original_url(session, short_code)
    if not url:
        raise HTTPException(
            status_code=404,
            detail='Short URL not found'
        )
    if url.owner_id and url.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to edit this URL"
        )
    response = await update_url(session, short_code, data)
    return URLResponse(
        original_url=response.original_url, short_code=response.short_code,
        created_at=response.created_at, expires_at=response.expires_at,
        owner_id=url.owner_id
    )


@router.delete(
    "/{short_code}", response_model=dict, status_code=HTTPStatus.OK
)
async def delete_short_url(
    short_code: str, session: AsyncSession = Depends(get_async_session),
    user: User = Depends(fastapi_users.current_user(active=True))
):

    url = await get_original_url(session, short_code)
    if not url:
        raise HTTPException(
            status_code=404,
            detail='Short URL not found'
        )
    if url.owner_id and url.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this URL"
        )

    await delete_url(session, short_code)
    return {'message': 'Short URL deleted'}


@router.get(
    "/{short_code}/stats", response_model=URLStatsResponse,
    status_code=HTTPStatus.OK
)
async def url_stats(
    short_code: str, session: AsyncSession = Depends(get_async_session)
):
    url = await get_url_stats(session, short_code)
    return URLStatsResponse(
        original_url=url.original_url, created_at=url.created_at,
        visit_count=url.visit_count, last_accessed=url.last_accessed
    )
