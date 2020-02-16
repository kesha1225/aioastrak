from astrak import Astrak, Dispatcher
from astrak.types import Message
import asyncio

astrak = Astrak(username="username", password="password")

dp = Dispatcher(astrak)


@dp.message_handler(text="привет")
async def text_handler(message: Message):
    await message.answer("И тебе привет!")


@dp.message_handler(text_contains="шуе")
async def text_handler(message: Message):
    await message.answer("ППШ")


loop = asyncio.get_event_loop()
loop.create_task(dp.dispatch_forever())
loop.run_forever()
