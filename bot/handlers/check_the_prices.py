from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import markdown_decoration as md

from bot.keyboards import coins_and_back, start_keyboard
from bot.states import CheckThePrices
from parser import binance_parse

check_the_prices_router = Router(name='check_the_prices')


@check_the_prices_router.message(F.text == 'Check the prices')
async def check_the_prices(message: Message, state: FSMContext) -> None:
    await message.answer(text='Select a coin\.', reply_markup=coins_and_back())
    await state.set_state(CheckThePrices.check_the_prices)


@check_the_prices_router.message(CheckThePrices.check_the_prices)
async def chose_a_coin(message: Message, state: FSMContext) -> None:
    chosen_coin = message.text

    if chosen_coin == 'Back':
        await message.answer(text='What is next?', reply_markup=start_keyboard())
        await state.clear()
    else:
        match chosen_coin:
            case 'Bitcoin':
                pair = 'BTCUSDT'
            case 'Ethereum':
                pair = 'ETHUSDT'
            case 'Neo':
                pair = 'NEOUSDT'
            case 'Arbitrum':
                pair = 'ARBUSDT'
            case 'Ripple':
                pair = 'XRPUSDT'
            case 'Binance Coin':
                pair = 'BNBUSDT'
            case 'Cardano':
                pair = 'ADAUSDT'
            case 'Litecoin':
                pair = 'LTCUSDT'
            case _:
                await message.answer(text=f'You have entered {md.bold("not a correct")} coin\.\n'
                                          f'Please, choose it from the {md.italic("keyboard list")}\.',
                                     reply_markup=coins_and_back())

                return

        answer = await binance_parse(pair)
        price = answer[0]['price']
        price_before = price[:-9]
        price_after = price[len(price_before) + 1:-6]
        price = price_before + '\.' + price_after

        await message.answer(text=f'Current {md.bold(chosen_coin)} price is {md.code("$" + price)}\.')
