import asyncio
from typing import Any

import aiohttp


async def binance_parse(coin: str) -> dict:
    URL = 'https://api.binance.com/api/v3/ticker/price?symbol=' + coin

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            return await response.json()


async def main(coin: str) -> tuple[BaseException | Any]:
    return await asyncio.gather(binance_parse(coin))
