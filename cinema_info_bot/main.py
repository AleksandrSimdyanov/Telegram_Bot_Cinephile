from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio
import os
from app.handlers.user_handlers import user_router
from app.handlers.admin_handlers import admin_router
from app.database.models import async_main
from app.states.state_director_add import director_add_router
from app.states.state_director_delete import director_del_router
from app.states.state_director_edit import director_edit_router
from app.states.state_movie_add import movie_add_router
from app.states.state_movie_delete import movie_del_router
from app.states.state_movie_edit import movie_edit_router
from app.states.AI_state import ai_state_router

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


# функция main
async def main():
    await async_main()
    dp.include_routers(ai_state_router, director_add_router, director_edit_router, director_del_router, movie_add_router, movie_del_router, movie_edit_router, user_router, admin_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")