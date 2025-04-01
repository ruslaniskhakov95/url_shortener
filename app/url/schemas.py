from pydantic import BaseModel, HttpUrl, constr
from typing import Optional
from datetime import datetime


AliasType = constr(min_length=3, max_length=25)


class BaseURL(BaseModel):
    original_url: HttpUrl


class BaseShortURL(BaseModel):
    short_code: str


class URLCreate(BaseURL):
    custom_alias: Optional[AliasType] = None
    expires_at: Optional[datetime] = None


class URLUpdate(BaseModel):
    new_original_url: Optional[HttpUrl] = None
    new_url: Optional[AliasType] = None
    expires_at: Optional[datetime] = None


class URLResponse(BaseURL):
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime]
    owner_id: Optional[int]


class URLStatsResponse(BaseURL):
    created_at: datetime
    visit_count: int
    last_accessed: datetime
