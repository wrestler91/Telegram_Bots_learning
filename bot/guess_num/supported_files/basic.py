from typing import Any
# from supported_files.conf import API_TOKEN
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import Message, ContentType
from aiogram.filters import BaseFilter
from environs import Env


env = Env()              # Создаем экземпляр класса Env
env.read_env()           # Методом read_env() читаем файл .env и загружаем из него переменные в окружение 
                          
bot_token = env('BOT_TOKEN')     # Сохраняем значение переменной окружения в переменную bot_token
admin_id = env.int('ADMIN_ID')   # Преобразуем значение переменной окружения к типу int 
                                 # и сохраняем в переменной admin_id
print(bot_token, admin_id)

# bot: Bot = Bot(token=bot_token)
# dp: Dispatcher = Dispatcher()

# # Этот фильтр будет проверять наличие неотрицательных чисел
# # в сообщении от пользователя, и передавать в хэндлер их список
# class Is_Number(BaseFilter):
#     def __init__(self) -> None:
#         super().__init__()

#     async def __call__(self, message: Message) -> dict:
#         result = []
#         for word in message.text.split():
#             word = word.strip(',. ')
#             if word.isdigit():
#                 result.append(word)
#         if result:
#             return {'numbers': result}
        


# async def main():
#     await dp.start_polling(bot)
#     # await dp.run_polling(bot)