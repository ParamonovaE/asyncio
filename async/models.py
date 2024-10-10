import os
from dotenv import load_dotenv 
from sqlalchemy import Integer, String, Float
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


load_dotenv()

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
SessionDB = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):

    __tablename__ = "swapi_people"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(50))
    height: Mapped[str] = mapped_column(String(20))  
    mass: Mapped[str] = mapped_column(String(20))
    skin_color: Mapped[str] = mapped_column(String(50))
    homeworld: Mapped[str] = mapped_column(String(100))
    films: Mapped[str] = mapped_column(String(500))
    species: Mapped[str] = mapped_column(String(500))
    starships: Mapped[str] = mapped_column(String(500))
    vehicles: Mapped[str] = mapped_column(String(500))


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)