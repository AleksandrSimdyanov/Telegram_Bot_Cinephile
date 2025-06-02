from app.database.models import Director, Movie, async_session
from sqlalchemy import select

async def get_directors():
    async with async_session() as session:
        directors = await session.scalars(select(Director))
    return directors

async def get_movies():
    async with async_session() as session:
        movies = await session.scalars(select(Movie))
    return movies

async def get_director_by_id(director_id):
    async with async_session() as session:
        director = await session.scalar(select(Director).where(Director.id == director_id))
    return director

async def get_movie_by_id(movie_id):
    async with async_session() as session:
        movie = await session.scalar(select(Movie).where(Movie.id == movie_id))
    return movie

async def movies_by_director_id(dir_id):
    async with async_session() as session:
        mov_by_dir_id = await session.scalars(select(Movie).where(Movie.director_id == dir_id))
    return mov_by_dir_id

async def add_director(name, info, photo):
    async with async_session() as session:
        dir = Director(name=name, info=info, photo=photo)
        session.add(dir)
        await session.commit()

async def del_director(director_id):
    async with async_session() as session:
        director = await session.scalar(select(Director).where(Director.id == director_id))
        await session.delete(director)
        await session.commit()

async def edit_director(director_id, name=None, info=None, photo=None):
    async with async_session() as session:
        director = await session.scalar(select(Director).where(Director.id == director_id))
        if name:
            director.name = name
        elif info:
            director.info = info
        elif photo:
            director.photo = photo
        await session.commit()

async def add_movie(name, info, photo):
    async with async_session() as session:
        mov = Movie(name=name, info=info, photo=photo)
        session.add(mov)
        await session.commit()

async def del_movie(movie_id):
    async with async_session() as session:
        movie = await session.scalar(select(Movie).where(Movie.id == movie_id))
        await session.delete(movie)
        await session.commit()

async def edit_movis(movie_id, name=None, info=None, photo=None):
    async with async_session() as session:
        movie = await session.scalar(select(Movie).where(Movie.id == movie_id))
        if name:
            movie.name = name
        elif info:
            movie.info = info
        elif photo:
            movie.photo = photo
            await session.commit()