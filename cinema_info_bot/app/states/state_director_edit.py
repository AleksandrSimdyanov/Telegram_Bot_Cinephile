from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from app import keyboards as kb
from app.database.requests import get_director_by_id, edit_director

director_edit_router = Router()

class EditDirector(StatesGroup):
    director_id = State()
    choice = State()
    name = State()
    info = State()
    photo = State()

@director_edit_router.callback_query(F.data == "admin_director_change")
async def start_edit_director(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Какого режиссера хотите изменить?", reply_markup=await kb.directors_kb(back=False))
    await state.set_state(EditDirector.director_id)
    await call.answer()

@director_edit_router.callback_query(EditDirector.director_id)
async def edit_director_func(call: CallbackQuery, state: FSMContext):
    director_id = call.data.split("_")[1]
    director = await get_director_by_id(director_id)
    await state.update_data(director_id=director_id)
    await state.set_state(EditDirector.choice)
    await call.message.edit_text(f"{director.name}\n"
                                 f"Что хотите поменять?", reply_markup=kb.admin_director_edit_kb)

@director_edit_router.callback_query(EditDirector.choice)
async def edit_choice(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")[2]
    if data == "name":
        await state.set_state(EditDirector.name)
        await call.message.edit_text("Введите новое имя режиссера")
    elif data == "info":
        await state.set_state(EditDirector.info)
        await call.message.edit_text("Введите новое описание для режиссера")
    elif data == "photo":
        await state.set_state(EditDirector.photo)
        await call.message.edit_text("Пришлите новое фото для режиссера")
    await call.answer()

async def save_changes(message: Message, text, state: FSMContext):
    data = await state.get_data()
    await edit_director(**data)
    await state.clear()
    await message.answer(f"{text} изменено")

@director_edit_router.message(EditDirector.name)
async def edit_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await save_changes(message, "Имя", state)

@director_edit_router.message(EditDirector.info)
async def edit_info(message: Message, state: FSMContext):
    info = message.text
    await state.update_data(info=info)
    await save_changes(message, "Описание", state)

@director_edit_router.message(EditDirector.photo)
async def edit_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    await state.update_data(photo=photo_file_id)
    await save_changes(message, "Фото", state)