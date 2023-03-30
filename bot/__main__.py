import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy import URL

from commands import commands
from commands import commands_routers
from handlers import handlers_routers
from bot.database import BaseModel, create_async_engine, get_session_maker, proceed_schemas


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = list()

    for command in commands:
        commands_for_bot.append(BotCommand(command=command[0], description=command[1]))

    dp = Dispatcher()
    bot = Bot(token=os.getenv('token'), parse_mode='MarkdownV2')
    postgres_url = URL.create(drivername='postgresql+asyncpg', host='localhost', port=os.getenv('db_port'),
                              database=os.getenv('db_name'), username=os.getenv('db_user'),
                              password=os.getenv('db_password'))
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await bot.set_my_commands(commands=commands_for_bot)

    for commands_router in commands_routers:
        dp.include_router(commands_router)

    for handlers_router in handlers_routers:
        dp.include_router(handlers_router)

    await proceed_schemas(async_engine, BaseModel.metadata)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('The bot has been stopped.')
