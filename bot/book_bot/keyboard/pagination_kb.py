'''кнопки под сообщением со страницей книги'''
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.handling import book

# Функция, генерирующая клавиатуру для страницы книги
def pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками при помощи лист компрехеншн
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON.get(button, button),
        callback_data=button) for button in buttons])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_pagination_keyboard(page=1):
    '''
    Функция обертка для клавиатуры, чтобы отображдать кнопки перехода в соответсвие с текущей страницей
    '''
    middle_buton = f'{page}/{len(book)}'
    if page == 1:
        return pagination_keyboard(middle_buton, 'forward')
    elif 1 < page < len(book):
        return pagination_keyboard('backward', middle_buton, 'forward')
    else:
        return pagination_keyboard('backward', middle_buton)
