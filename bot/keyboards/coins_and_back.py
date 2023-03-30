from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def coins_and_back() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Bitcoin'), KeyboardButton(text='Ethereum'), KeyboardButton(text='Neo'),
            KeyboardButton(text='Arbitrum')],
        [KeyboardButton(text='Ripple'), KeyboardButton(text='Binance Coin'), KeyboardButton(text='Cardano'),
            KeyboardButton(text='Litecoin')], [KeyboardButton(text='Back')]], resize_keyboard=True)
