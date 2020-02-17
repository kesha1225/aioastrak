import aiohttp
from .types import Me, Dialog, DialogMessage, Event
from .exceptions import AstrakServerException, AstrakException
import asyncio
import typing
import logging


class Astrak:
    def __init__(
        self,
        token: str = None,
        username: str = None,
        password: str = None,
        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
    ):
        self.loop = loop
        self.host = "http://afternoon-dusk-97603.herokuapp.com/{}"
        self.session = aiohttp.ClientSession()
        self._token = token
        self.username = username
        self.password = password

    @property
    async def token(self) -> str:
        if self._token is None:
            self._token = (await self.get_me()).token
        return self._token

    async def _api_request(self, api_method, method="post", **data) -> dict:
        logging.debug(f"Making request on /{api_method} with data - {data}")
        async with self.session.request(
            method=method, url=self.host.format(api_method), data=data
        ) as resp:
            if resp.content_type != "application/json":
                raise AstrakServerException(await resp.text())
            json_resp = await resp.json()
            if json_resp["code"] < 0:
                raise AstrakException(json_resp["response"])
            return json_resp

    async def get_me(self) -> Me:
        return Me(
            **await self._api_request(
                api_method="users/login", username=self.username, password=self.password
            )
        )

    async def check_token(self, token: str) -> dict:
        return await self._api_request(api_method="users/check", token=token)

    async def send_message(self, text: str, to_id: int) -> dict:
        return await self._api_request(
            api_method="messages/send", token=await self.token, text=text, to=to_id
        )

    async def get_dialog(self, user_id: int) -> typing.List[DialogMessage]:
        raw_dialog = await self._api_request(
            method="get",
            api_method="messages/dialog",
            token=await self.token,
            id=user_id,
        )
        dialog_messages = []

        for dialog_message in raw_dialog["response"]:
            dialog_messages.append(DialogMessage(**dialog_message))

        return dialog_messages

    async def get_all_dialogs(self) -> typing.List[Dialog]:
        raw_dialogs = await self._api_request(
            method="get", api_method="messages/dialogs", token=await self.token
        )
        dialogs = []

        for dialog in raw_dialogs["response"]:
            dialogs.append(Dialog(**dialog))
        return dialogs

    async def get_events(self) -> Event:
        event = await self._api_request(
            api_method="events/polling", token=await self.token
        )
        return Event(type=event["type"], event=event["event"])
