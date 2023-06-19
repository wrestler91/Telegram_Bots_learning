import asyncio
import logging

from aiogram import Bot, Dispatcher
from configs.config import Configs, load_configs
from handlers import other_handlers, user_handlers
from keyboard.main_menu import set_main_menu
from services.handling import prepare_book

# Инициализируем логгер
logger = logging.getLogger(__name__)
BOOK_PATH = 'C:/Users/Арутюн/Desktop/python/проекты/телеграм-бот/бот_из_курса/bot/book_bot/book/book.txt'
# BOOK_PATH ='bot/book_bot/book/book.txt'

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Configs = load_configs()

    # готовим книгу для тг бота при помощ инашей функции
    prepare_book(path=BOOK_PATH)
    

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


    