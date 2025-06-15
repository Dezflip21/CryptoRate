import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp

# Вставьте сюда ваш токен
TOKEN = '8041361674:AAEbzFfzFlfM_jo8mY3gHq2nG_GvOm9YXmA'

bot = Bot(token=TOKEN)
dp = Dispatcher()

cryptos = {
    'Bitcoin': 'bitcoin',
    'Ethereum': 'ethereum',
    'Litecoin': 'litecoin',
    'Ripple': 'ripple',
    "Dogecoin": "dogecoin",
    "Bitcoin Cash": "bitcoin-cash",
    "Cardano": "cardano",
    "Polkadot": "polkadot",
    "Stellar": "stellar",
    "Chainlink": "chainlink",
    "Binance Coin": "binancecoin",
    "Tether": "tether",
    "Solana": "solana",
    "Uniswap": "uniswap",
    "Monero": "monero",
    "EOS": "eos",
    "TRON": "tron"
}


async def get_prices(crypto_ids):
    ids_param = ','.join(crypto_ids)
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data
    except:
        return None


@dp.message(Command(commands=["start"]))
async def start_handler(message: types.Message):
    # Получаем цены всех криптовалют
    crypto_ids = list(cryptos.values())
    data = await get_prices(crypto_ids)

    if data:
        # Формируем сообщение со списком криптовалют и их ценами
        message_text = "Текущие курсы криптовалют:\n\n"
        for name, id in cryptos.items():
            price = data.get(id, {}).get('usd', 'N/A')
            message_text += f"{name}: ${price}\n"
        await message.answer(message_text)
    else:
        await message.answer("Не удалось получить данные о курсах.")


@dp.message()
async def handle_message(message: types.Message):
    choice = message.text
    if choice in cryptos:
        price = await get_price(cryptos[choice])
        if price is not None:
            await message.answer(f"{choice} стоит ${price}")
        else:
            await message.answer("Не удалось получить данные.")
    else:
        await message.answer("Пожалуйста, используйте /start для получения курсов.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())