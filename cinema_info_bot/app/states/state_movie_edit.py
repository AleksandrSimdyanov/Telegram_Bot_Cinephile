from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app import keyboards as kb
from app.database.models import Movie

from app.database.requests import get_movie_by_id, edit_movis

movie_edit_router = Router()

class EditMovie(StatesGroup):
    movie_id = State()
    choice = State()
    name = State()
    info = State()
    photo = State()

@movie_edit_router.callback_query(F.data == "admin_movie_change")
async def start_edit_movie(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Какой фильм хотите изменить?", reply_markup=await kb.movies_kb(back=False))
    await state.set_state(EditMovie.movie_id)
    await call.answer()

@movie_edit_router.callback_query(EditMovie.movie_id)
async def edit_movie_func(call: CallbackQuery, state: FSMContext):
    movie_id = call.data.split("_")[1]
    movie = await get_movie_by_id(movie_id)
    await state.update_data(movie_id=movie_id)
    await state.set_state(EditMovie.choice)
    await call.message.edit_text(f"{movie.name}"
                                 f"Что хотите изменить?", reply_markup=kb.admin_movie_edit_kb)

@movie_edit_router.callback_query(EditMovie.choice)
async def edit_choice(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")[2]
    if data == "name":
        await state.set_state(EditMovie.name)
        await call.message.edit_text("Введите новое имя фильма")
    elif data == "info":
        await state.set_state(EditMovie.info)
        await call.message.edit_text("Введите новое описание для фильма")
    elif data == "photo":
        await state.set_state(EditMovie.photo)
        await call.message.edit_text("Пришлите новое фото для фильма")
    await call.answer()

async def save_changes(message: Message, text, state: FSMContext):
    data = await state.get_data()
    await edit_movis(**data)
    await state.clear()
    await message.answer(f"{text} изменено")

@movie_edit_router.message(EditMovie.name)
async def edit_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await save_changes(message, "Имя", state)

@movie_edit_router.message(EditMovie.info)
async def edit_info(message: Message, state: FSMContext):
    info = message.text
    await state.update_data(info=info)
    await save_changes(message, "Описание", state)

@movie_edit_router.message(EditMovie.photo)
async def edit_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    await state.update_data(photo=photo_file_id)
    await save_changes(message, "Фото", state)