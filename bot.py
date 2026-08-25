from aiogram import Bot, Dispatcher #bot - связывание токена с ботом/ диспетчер 
from aiogram.types import Message # для обработки текста от юзера
import asyncio # для асинхронного запуска

from handlers import commands_router # импорт роутера(старт, инфо)
from handlers.download import router as download_router #импорт роутера скачивания

bot = Bot(token="7955059770:AAGOBqrS3lV5zhIobO6nTr55U0aQqMeemf0")  #инициализация бота
dp = Dispatcher(bot=bot) #инициализация диспетчера

#подключение роутеров
dp.include_router(commands_router)
dp.include_router(download_router)

#асинхронное получение инфы от тг(бота)
async def main():
    await dp.start_polling(bot)

#асинхронный запуск
if __name__ == "__main__":
    asyncio.run(main())