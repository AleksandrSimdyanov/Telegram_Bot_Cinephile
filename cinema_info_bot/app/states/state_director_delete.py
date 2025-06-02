from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app import keyboards as kb
from app.database.requests import del_director

director_del_router = Router()

class DelDirector(StatesGroup):
    director_id = State()

@director_del_router.callback_query(F.data == "admin_director_delete")
async def del_director_director_id(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Какого режиссера хотите удалить?", reply_markup=await kb.directors_kb(back = False))
    await state.set_state(DelDirector.director_id)
    await call.answer()

@director_del_router.callback_query(DelDirector.director_id)
async def del_director_id(call: CallbackQuery, state: FSMContext):
    director_id = call.data.split("_")[1]
    await state.clear()
    await call.message.edit_text("Режиссер удален")
    await del_director(director_id)