from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import markdown_decoration as md
from sqlalchemy import Result, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import User, UserCoin
from bot.keyboards import coins_and_back, start_keyboard
from bot.states import DailyAlerts
from bot.filters import IsCoinOrBack

daily_alerts_router = Router(name='check_the_prices')


@daily_alerts_router.message(F.text == 'Daily alerts')
async def check_the_prices(message: Message, state: FSMContext) -> None:
    await message.answer(text='Select a coin which price you want to track\.', reply_markup=coins_and_back())
    await state.set_state(DailyAlerts.daily_alerts)


@daily_alerts_router.message(DailyAlerts.daily_alerts, IsCoinOrBack())
async def chose_a_coin(message: Message, state: FSMContext, session_maker: sessionmaker) -> None:
    chosen_coin: str = message.text

    if chosen_coin == 'Back':
        await message.answer(text='What is next?', reply_markup=start_keyboard())
        await state.clear()
    else:
        session: AsyncSession
        user_telegram_id: int = message.from_user.id

        async with session_maker() as session:
            async with session.begin():
                user_query: Result = await session.execute(select(User).where(User.telegram_id == user_telegram_id))
                user: User = user_query.one_or_none()[0]
                user_coins_query: Result = await session.execute(
                    select(UserCoin.coin).where(UserCoin.user_id == user.id))
                user_coins: list[str] = [coin_tuple[0] for coin_tuple in user_coins_query.all()]

                if chosen_coin in user_coins:
                    await message.answer(text=f'You already track {md.bold(chosen_coin)}\.')
                else:
                    await session.execute(insert(UserCoin).values(user_id=user.id, coin=chosen_coin))
                    await message.answer(text=f'Alright\! You now track {md.bold(chosen_coin)}\.\n'
                                              f'Now prepare to receive daily notifications about its price\.')
