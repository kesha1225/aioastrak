from astrak import Astrak, Dispatcher, TaskManager
from astrak.types import Message
import logging

logging.basicConfig(level=logging.DEBUG)

astrak = Astrak(username="username", password="password")
dp = Dispatcher(astrak)


@dp.message_handler(text="привет")
async def text_handler(message: Message):
    await message.answer("И тебе привет!")


@dp.message_handler(text_contains="шуе")
async def text_handler(message: Message):
    await message.answer("ППШ")


task_manager = TaskManager(astrak.loop)
task_manager.add_task(dp.dispatch_forever())
task_manager.run()
