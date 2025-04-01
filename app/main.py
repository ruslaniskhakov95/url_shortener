import uvicorn
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from redis import asyncio as aioredis

from scheduler import init_scheduler
from url.router import router as url_router
from user.router import router as auth_router


scheduler = init_scheduler()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="URL Shortener",
    description="URL Shortener service",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="URL Shortener API",
        version="1.0.0",
        description="API for URL shortening service with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    global scheduler
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    global scheduler
    scheduler.shutdown(wait=True)


app.include_router(auth_router)
app.include_router(url_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
