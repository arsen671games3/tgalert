import socket
import enum
from enum import auto
import logging
import traceback
import inspect
from contextlib import asynccontextmanager
from typing import Union

import aiohttp


log = logging.getLogger(__name__)


class Language(enum.Enum):
    en = auto()
    ru = auto()


class TGAlert:
    def __init__(
            self,
            bot_token: str,
            alert_chat: Union[str, int],
            node_name: str = None,
            language: Language = Language.en,
    ):
        # alert_chat is the id or username of the chat where the alerts will be sent.
        # Attention! You cannot use the username of user because of a telegram bot api error.
        # alert_chat это id или username чата, куда будут отправляться алерты.
        # Внимание! Нельзя использовать username пользователя из-за ошибки telegram bot api.
        if bot_token:
            self.bot_token = bot_token
        else:
            self.bot_token = None
            log.warning('bot_token is empty. Messages will not be sent.')
        self.alert_chat = alert_chat
        self.session = None
        self.node_name = (node_name or socket.getaddrinfo(
            socket.gethostname(), 0, flags=socket.AI_CANONNAME
        )[0][3])
        self.language = language

    async def __aenter__(self, *args):
        await self.start()

    async def __aexit__(self, *args):
        await self.stop()

    async def start(self):
        self.session = aiohttp.ClientSession()
        return self

    async def stop(self):
        return await self.session.close()

    async def send_alert(self, error_text: str):
        if self.bot_token is None:
            return
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        params = {'chat_id': self.alert_chat, 'text': error_text[:4096], 'parse_mode': 'HTML',
                  'disable_notification': 'false'}
        async with self.session.post(url, params=params) as response:
            if response.status == 200:
                return
            else:
                raise RuntimeError(await response.text())

    @asynccontextmanager
    async def catch_alert(self, *format_args, reraise=True, **format_kwargs):
        try:
            yield
        except Exception as e:
            log.error(e, exc_info=True)
            tb = '<b>'+str(e)+'</b>' + '\n' + self._html_escape(traceback.format_exc())

            function_name = inspect.stack()[2].function

            await self.send_alert(self.format(function_name, tb, *format_args, **format_kwargs))
            if reraise:
                raise

    @staticmethod
    def _html_escape(text: str) -> str:
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def format(self, function_name: str, tb: str) -> str:
        if self.language == Language.en:
            return (f'There was an error on node {self.node_name} in function '
                    f'<b>{function_name}</b>:\n{tb}')
        elif self.language == Language.ru:
            return (f'На ноде {self.node_name} в функции <b>{function_name}</b> произошла ошибка:\n'
                    f'{tb}')
        else:
            raise NotImplementedError()
