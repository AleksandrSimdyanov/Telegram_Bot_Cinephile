from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from app import keyboards as kb
import app.database.requests as rq

user_router = Router()

@user_router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("🍿Привет, киноман\n"
                 "🔍Для поиска используйте кнопки ниже или отправь в сообщении название кино", reply_markup=kb.start_kb)


@user_router.callback_query(F.data == "all_directors")
async def send_directors(call: CallbackQuery):
    await call.message.edit_text("Какой режиссер Вас интересует?", reply_markup= await kb.directors_kb())
    await call.answer()


@user_router.callback_query(F.data == "all_films")
async def send_movies(call: CallbackQuery):
    await call.message.edit_text("Какой фильм Вас интересует?", reply_markup=await kb.movies_kb())
    await call.answer()

@user_router.callback_query(F.data.startswith("director_"))
async def show_director_info(call: CallbackQuery):
    director_id = int(call.data.split("_")[1])
    director = await rq.get_director_by_id(director_id)
    if director.photo.endswith(".png"):
        photo = FSInputFile(f"app/database/images/directors/{director.photo}")
    else:
        photo = director.photo
    information = director.info
    media = InputMediaPhoto(media=photo, caption=information)
    await call.message.edit_media(media=media, reply_markup= await kb.movies_by_director_kb(director.id))
    await call.answer()

@user_router.callback_query(F.data.startswith("movie_"))
async def show_movie_info(call: CallbackQuery):
    movie_id = int(call.data.split("_")[1])
    movie = await rq.get_movie_by_id(movie_id)
    photo = FSInputFile(f"app/database/images/films/{movie.photo}")
    information = movie.info
    media = InputMediaPhoto(media=photo, caption=information)
    await call.message.edit_media(media=media, reply_markup= await kb.director_by_movie_kb(movie.id))
    await call.answer()

@user_router.callback_query(F.data.startswith("back"))
async def get_back(call: CallbackQuery):
    data = call.data.split("_")[1]
    if data == "menu":
        await call.message.edit_text("🍿Привет, киноман\n"
                             "🔍Для поиска используйте кнопки ниже или отправь в сообщении название кино",
                             reply_markup=kb.start_kb)
        await call.answer()
    elif data == "movie":
        await call.message.delete()
        await call.message.answer("Какой режиссер Вас интересует?", reply_markup=await kb.directors_kb())
        await call.answer()
    elif data == "director":
        await call.message.delete()
        await call.message.answer("Какой фильм Вас интересует?", reply_markup=await kb.movies_kb())
        await call.answer()