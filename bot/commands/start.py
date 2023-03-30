from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import markdown_decoration as md
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.baked import Result
from sqlalchemy.orm import sessionmaker

from bot.database import User, UserCoin

from bot.keyboards import start_keyboard

start_router = Router(name='start')


@start_router.message(Command(commands=['start']))
async def start(message: Message, session_maker: sessionmaker) -> None:
    session: AsyncSession

    async with session_maker() as session:
        async with session.begin():
            result: Result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
            user: User = result.one_or_none()[0]

            if user:
                coins_result: Result = await session.execute(select(UserCoin.coin).where(UserCoin.user_id == user.id))
                coins: list[str] = [md.bold(coin_tuple[0]) for coin_tuple in coins_result.all()]
            else:
                user = User(telegram_id=message.from_user.id, full_name=message.from_user.full_name,
                            username=message.from_user.username)

                await session.merge(user)

    text = f'Hello, {md.bold(message.from_user.full_name)}\.\n\n' \
           'With my help you can always keep in touch with cryptocurrency\.'

    if len(coins) > 0:
        italic_text = 'You track the following coins: ' + ', '.join(coins) + '\.'

        await message.answer(text=text + f'\n\n{md.italic(italic_text)}', reply_markup=start_keyboard())
    else:
        italic_text = 'You do not track any coin'

        await message.answer(text=text + f'\n\n{md.italic(italic_text)}\.', reply_markup=start_keyboard())
