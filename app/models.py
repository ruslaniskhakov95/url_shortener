from datetime import datetime, timezone
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String
)
from sqlalchemy.ext.declarative import declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    urls = relationship("ShortURL", back_populates='owner')


class ShortURL(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    expires_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc),
        nullable=True
    )
    visit_count = Column(Integer, default=0)
    last_accessed = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc),
        nullable=True
    )

    owner_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True
    )
    owner = relationship('User', back_populates='urls')
