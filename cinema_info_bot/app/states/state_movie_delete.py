from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app import keyboards as kb
from app.database.requests import del_movie

movie_del_router = Router()

class DelMovie(StatesGroup):
    movie_id = State()

@movie_del_router.callback_query(F.dat == "admin_movie_delete")
async def del_movie_movie_id(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Какой фильм хотите удалить?", reply_markup= await kb.movies_kb(back=False))
    await state.set_state(DelMovie.movie_id)
    await call.answer()

@movie_del_router.callback_query(DelMovie.movie_id)
async def del_movie_id(call: CallbackQuery, state: FSMContext):
    movie_id = call.data.split("_")[1]
    await state.clear()
    await call.message.edit_text("Режиссер удален")
    await del_movie(movie_id)