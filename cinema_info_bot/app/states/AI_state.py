from aiogram.filters import Command
import requests
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

load_dotenv()

def answer_ai(description):
    API_key = os.getenv("API_key")
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_key}"
    }
    model = 'deepseek-ai/DeepSeek-R1'
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Найди фильм по его описанию"
            },
            {
                "role": "user",
                "content": description
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()["choices"][0]["message"]["content"].split("</think>\n\n")[1]
    return content

ai_state_router = Router()

class AI(StatesGroup):
    description = State()

@ai_state_router.message(Command("search_movie"))
async def search_movie(message: Message, state: FSMContext):
    await message.answer("Введите описание по фильму, который хотите найти:")
    await state.set_state(AI.description)

@ai_state_router.message(AI.description)
async def add_description(message: Message, state: FSMContext):
    description = message.text
    await message.answer(answer_ai(description), parse_mode="Markdown")
    await state.clear()