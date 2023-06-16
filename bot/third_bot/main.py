from aiogram import Bot, Dispatcher
import asyncio
from configs.config import Configs, load_configs
from handlers import user_handlers, other_handles

# Создаем объекты бота и диспетчера
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Configs = load_configs()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handles.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())