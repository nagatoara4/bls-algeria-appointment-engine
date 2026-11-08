import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.services.db import init_db
from bot.services.monitor import restore_monitors
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.handlers import start, booking, monitor, admin, common

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    await init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(ThrottlingMiddleware(0.6))

    dp.include_router(start.router)
    dp.include_router(booking.router)
    dp.include_router(monitor.router)
    dp.include_router(admin.router)
    dp.include_router(common.router)

    await restore_monitors(bot)
    logger.info("BLS Algeria Appointment Engine v2 started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
