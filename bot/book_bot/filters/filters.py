'''Создаем два пользовательских фильтра'''

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    '''
    проверяет состоят ли данные объекта callback из цифр,
    так мы понимаем что была нажат кнопка сохраненния закладки
    '''
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and callback.data.isdigit()
    


class IsDelBookmarkCallbackData(BaseFilter):
    '''
    ловит callback в котормо есть текст del, 
    так мы понимаем, что нажата кнопка удаления закладки
    '''
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'del'         \
            in callback.data and callback.data[:-3].isdigit()

