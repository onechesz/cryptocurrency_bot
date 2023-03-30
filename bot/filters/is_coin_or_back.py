from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCoinOrBack(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        coins_or_back = ['Bitcoin', 'Ethereum', 'Neo', 'Arbitrum', 'Ripple', 'Binance Coin', 'Cardano', 'Litecoin',
                         'Back']

        return message.text in coins_or_back
