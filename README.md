

```
pip install https://github.com/kesha1225/aioastrak/archive/master.zip --upgrade
```

api
```python3
from astrak import Astrak
import asyncio

astrak_api = Astrak(username="username", password="password")


async def main():
    me = await astrak_api.get_me()
    print(me.id)

    dialogs = await astrak_api.get_all_dialogs()
    print(dialogs)

    await astrak_api.session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```


bot
```python3
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

```