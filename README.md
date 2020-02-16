

```
pip install https://github.com/kesha1225/aioastrak/archive/master.zip --upgrade
```

api
```python3
from astrak import Astrak
import asyncio

astrak_api = Astrak(username="username", password="username")


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

```