''''клавиатуры для работы с закладками пользователя'''
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.handling import book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    '''
    Функция для создания списка закладок
    В args передается множества номеров страниц в виде цифр
    '''
    
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args): 
        kb_builder.row(InlineKeyboardButton(
            # для отображения текста закладки, получаем доступ к тексту по ключу (номер страницы), 
            # и выводим первые 100 символов этой страницы
            text=f'{button} - {book[button][:100]}', 
            callback_data=str(button))) # здесь в callback_data передается номер страницы
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['edit_bookmarks_button'],
                        callback_data='edit_bookmarks'),
                   InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'),
                   width=2)
    return kb_builder.as_markup()

def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    '''
    Функция для созданяи списка закладок для редактирования
    '''
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {button} - {book[button][:100]}',
            callback_data=f'{button}del'))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'))
    return kb_builder.as_markup()



