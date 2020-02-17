from astrak import Astrak
import asyncio

astrak_api = Astrak(username="username", password="password")


async def main():
    me = await astrak_api.get_me()

    print(me.id)

    dialogs = await astrak_api.get_all_dialogs()

    print(dialogs)

    await astrak_api.send_message(text="123", to_id=1)
    await astrak_api.session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
