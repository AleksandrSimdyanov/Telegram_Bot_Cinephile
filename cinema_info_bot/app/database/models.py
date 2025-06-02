from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv
from sqlalchemy import String, ForeignKey
import os

load_dotenv()

# создаем ассинхронный движок базы данных с использованием URL
engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))

# переменная для подключения к базе данных
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Director(Base):
    __tablename__ = 'directors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    info: Mapped[str] = mapped_column(String(1000))
    photo: Mapped[str] = mapped_column(String(100))

class Movie(Base):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    info: Mapped[str] = mapped_column(String(1000))
    photo: Mapped[str] = mapped_column(String(100))
    director_id: Mapped[int] = mapped_column(ForeignKey('directors.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
