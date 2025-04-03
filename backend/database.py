from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 두 가지 URL 설정 (하나는 비동기, 하나는 동기)
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app.db"
SYNC_SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# 비동기 엔진 (FastAPI 앱용)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# 동기 엔진 (Alembic용)
sync_engine = create_engine(SYNC_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()

# 비동기 DB 의존성 (FastAPI용)
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()