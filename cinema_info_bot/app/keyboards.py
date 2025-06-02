from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.database.requests as rq

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Режиссеры🎥👦", callback_data="all_directors"), InlineKeyboardButton(text="Фильмы🎞", callback_data="all_films")]
    ]
)

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Фильмы", callback_data="admin_movies"), InlineKeyboardButton(text="Режиссеры", callback_data="admin_directors")]
    ]
)

admin_director_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить режиссера", callback_data="admin_director_delete")],
        [InlineKeyboardButton(text="Добавить режиссера", callback_data="admin_director_add")],
        [InlineKeyboardButton(text="Изменить режиссера", callback_data="admin_director_change")],
        [InlineKeyboardButton(text="⏪Вернуться", callback_data="admin_back")]
    ]
)

admin_movie_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить фильм", callback_data="admin_movie_delete")],
        [InlineKeyboardButton(text="Добавить фильм", callback_data="admin_movie_add")],
        [InlineKeyboardButton(text="Изменить филльм", callback_data="admin_movie_change")],
        [InlineKeyboardButton(text="⏪Вернуться", callback_data="admin_back")]
    ]
)

admin_director_edit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать имя", callback_data="director_edit_name")],
        [InlineKeyboardButton(text="Редактировать описание", callback_data="director_edit_info")],
        [InlineKeyboardButton(text="Редактировать фото", callback_data="director_edit_photo")]
    ]
)

admin_movie_edit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать название", callback_data="movie_edit_name")],
        [InlineKeyboardButton(text="Редактировать описание", callback_data="movie_edit_info")],
        [InlineKeyboardButton(text="Редактировать фото", callback_data="movie_edit_photo")]
    ]
)

async def directors_kb(back = True):
    builder = InlineKeyboardBuilder()
    directors = await rq.get_directors()
    for director in directors:
        button = InlineKeyboardButton(text=director.name, callback_data=f"director_{director.id}")
        builder.add(button)
    builder.adjust(2)
    if back:
        builder.row(InlineKeyboardButton(text="⏪Вернуться", callback_data="back_menu"))
    return builder.as_markup()

async def movies_kb(back = True):
    builder = InlineKeyboardBuilder()
    movies = await rq.get_movies()
    for movie in movies:
        button = InlineKeyboardButton(text=movie.name, callback_data=f"movie_{movie.id}")
        builder.add(button)
    builder.adjust(2)
    if back:
        builder.row(InlineKeyboardButton(text="⏪Вернуться", callback_data="back_menu"))
    return builder.as_markup()

async def movies_by_director_kb(d_id):
    builder = InlineKeyboardBuilder()
    movies = await rq.movies_by_director_id(d_id)
    for movie in movies:
        button = InlineKeyboardButton(text = movie.name, callback_data=f"movie_{movie.id}")
        builder.add(button)
    builder.row(InlineKeyboardButton(text="⏪Вернуться", callback_data="back_movie"))
    return builder.as_markup()

async def director_by_movie_kb(m_id):
    movie = await rq.get_movie_by_id(m_id)
    director = await rq.get_director_by_id(movie.director_id)
    dir_by_mov_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=director.name, callback_data=f"director_{director.id}")],
            [InlineKeyboardButton(text="⏪Вернуться", callback_data="back_director")]
        ]
    )
    return dir_by_mov_kb