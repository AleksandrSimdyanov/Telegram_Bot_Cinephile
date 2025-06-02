from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app import keyboards as kb

admin_router = Router()

@admin_router.message((F.text == "/admin") & (F.from_user.id == 835168779))
async def admin_cmd(message: Message):
    await message.answer("Это панель администратора. Выберите пункт меню:", reply_markup=kb.admin_kb)

@admin_router.callback_query(F.data.startswith("admin_directors"))
async def admin_director(call: CallbackQuery):
    await call.message.edit_text("Выберите действие", reply_markup=kb.admin_director_kb)
    await call.answer()

@admin_router.callback_query(F.data.startswith("admin_movies"))
async def movie_director(call: CallbackQuery):
    await call.message.edit_text("Выберите действие", reply_markup=kb.admin_movie_kb)
    await call.answer()

@admin_router.callback_query(F.data == "admin_back")
async def back(call: CallbackQuery):
    await call.message.edit_text("Это панель администратора. Выберите пункт меню:", reply_markup=kb.admin_kb)