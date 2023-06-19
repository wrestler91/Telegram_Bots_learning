from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboard.bookmarks import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboard.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.handling import book

# Инициализируем роутер уровня модуля
router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'],
                        reply_markup=ReplyKeyboardRemove())
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

# срабатывает на команду /help
@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(text=LEXICON['/help'])

# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    # здесь сохраняем страницу на которйо останавлиается пользователь 
    # т.к. он только начал читать, то и страница 1-я
    page = users_db[message.from_user.id]['page'] = 1
    # здесь по ключу номера текущей стринцы у пользователя выволдим текст
    text = book[page]
    await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(page))
    
# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    page = users_db[message.from_user.id]['page']
    text = book[page]
    await message.answer(
                text=text,
                reply_markup=create_pagination_keyboard(page))
   

# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text], # здесь message.text == bookmarks
            # здесь выводим список закладок при помощи нашей функции
            # в котору передаем списко сохраненных закладок пользоаателя
            # которые доступны по специальному ключу
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(Text(text=['forward', 'backward']))
async def process_forward_press(callback: CallbackQuery):
    # при каждом нажатии кнопки вперед, в соответсвующий списко (БД) прибавляем 1 страницу
    
    page = users_db[callback.from_user.id]['page'] 
    if callback.data == 'forward':
        page += 1
    elif callback.data == 'backward':
        page -= 1

    text = book[page]
    users_db[callback.from_user.id]['page'] = page

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(page))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    # В нашу БД добавляем номер закладки
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']) # номер сохраняемой странички берется из БД поля текущей страницы пользователя
    await callback.answer('Страница добавлена в закладки!')

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
# то есть будет переход на закладку
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    page = int(callback.data)
    # получаем текст закладки
    text = book[page]
    # сохраняем текущую страницу пользователя
    users_db[callback.from_user.id]['page'] = page
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(page))
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок для удаления
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    # получаем закладку из колл-бека
    mark = int(callback.data[:-3]) # здесь из сообщения удаляет del (3 последних символа)
    # удаляем ее из нашей БД
    users_db[callback.from_user.id]['bookmarks'].remove(mark)
    # если есть еще закладки в БД, то отображаем оставшиеся закладки
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
                    text=LEXICON['/bookmarks'],
                    reply_markup=create_edit_keyboard(
                            *users_db[callback.from_user.id]["bookmarks"]))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
