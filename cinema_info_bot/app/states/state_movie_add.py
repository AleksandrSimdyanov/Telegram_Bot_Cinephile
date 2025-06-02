from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.requests import add_movie

movie_add_router = Router()

class AddMovie(StatesGroup):
    name = State()
    info = State()
    photo = State()

@movie_add_router.callback_query(F.data == "admin_movie_add")
async def show_admin_movie_panel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Давайте начнем добавление нового фильма."
                                 "Отправьте его название")
    await state.set_state(AddMovie.name)
    await call.answer()

@movie_add_router.message(AddMovie.name)
async def add_movie_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(AddMovie.info)
    await message.answer("Введите информацию о режиссере")

@movie_add_router.message(AddMovie.info)
async def add_movie_info(message: Message, state: FSMContext):
    info = message.text
    await state.update_data(info=info)
    await state.set_state(AddMovie.photo)
    await message.answer("Пришлите фото фильма")

@movie_add_router.message(AddMovie.photo)
async def add_movie_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    await message.answer("Режиссер добавлен")
    await add_movie(data["name"], data["info"], data["photo"])