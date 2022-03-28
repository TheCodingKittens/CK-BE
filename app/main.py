import aioredis
from aredis_om.connections import get_redis_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api.api_v1.api import api_router
from app.utils.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, docs_url="/swagger", redoc_url="/docs")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(api_router)

    return _app


app = get_application()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.on_event("startup")
async def startup():
    r = aioredis.from_url(
        settings.REDIS_CACHE_URL, encoding="utf8", decode_responses=True
    )

    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    print("Start up Successful")
