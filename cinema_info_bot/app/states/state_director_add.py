from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.requests import add_director

director_add_router = Router()

class AddDirector(StatesGroup):
    name = State()
    info = State()
    photo = State()

@director_add_router.callback_query(F.data == "admin_director_add")
async def show_admin_director_panel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Давайте начнем добавление нового режиссера."
                      "Отправьте его имя и фамилию")
    await state.set_state(AddDirector.name)
    await call.answer()

@director_add_router.message(AddDirector.name)
async def add_director_name(message: Message, state: FSMContext):
    name = message.text
    if name.isdigit():
        await message.answer("Имя должно состоять из букв")
        return
    await state.update_data(name=name)
    await state.set_state(AddDirector.info)
    await message.answer("Введите информацию о режиссере")

@director_add_router.message(AddDirector.info)
async def add_director_info(message: Message, state: FSMContext):
    info = message.text
    await state.update_data(info=info)
    await state.set_state(AddDirector.photo)
    await message.answer("Пришлите фото режиссера")

@director_add_router.message(AddDirector.photo)
async def add_director_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file_id = photo.file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    await state.clear()
    await message.answer("Режиссер добавлен")
    print(data)
    await add_director(data["name"], data["info"], data["photo"])