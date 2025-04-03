import asyncio
import logging
from telethon import events
from .. import loader, utils

logger = logging.getLogger(__name__)

def register(cb):
    cb(AutoMessageMod())

class AutoMessageMod(loader.Module):
    """Auto Message Sender"""
    strings = {'name': 'AutoMessage'}

    def __init__(self):
        self.tasks = {}

    async def autolcmd(self, message):
        """Используй .autol <интервал в минутах> <текст>."""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit('<b>Нет аргументов после команды :c</b>')
            return

        try:
            t, text = args.split(' ', 1)
            t = int(t)
        except ValueError:
            await message.edit('<b>Неправильный формат аргументов :c</b>')
            return

        chat_id = message.chat_id
        if chat_id in self.tasks:
            await message.edit('<b>Уже выполняется задача для этого чата. Остановите её перед началом новой.</b>')
            return

        self.tasks[chat_id] = self._client.loop.create_task(self.send_message_periodically(chat_id, t, text))
        await message.edit(f'<b>Сообщение будет отправляться каждые {t} минут(ы).</b>')

    async def send_message_periodically(self, chat_id, interval, text):
        while True:
            await self._client.send_message(chat_id, text)
            await asyncio.sleep(interval * 60)

    async def alstopcmd(self, message):
        """Используй .alstop для остановки отправки сообщений."""
        chat_id = message.chat_id
        if chat_id in self.tasks:
            self.tasks[chat_id].cancel()
            del self.tasks[chat_id]
            await message.edit('<b>Автоматическая отправка сообщений остановлена.</b>')
        else:
            await message.edit('<b>Нет активной задачи для этого чата.</b>')
