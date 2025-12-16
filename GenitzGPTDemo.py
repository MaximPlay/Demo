from telethon import events
from .. import loader, utils
import asyncio
import requests

def register(cb):
    cb(GigaChatMod())

class GigaChatMod(loader.Module):
    strings = {"name": "GigaChat"}

    def __init__(self):
        self.name = self.strings["name"]
        self.me = None
        self.ratelimit = []
        self.api_key = "MDE5YjI2MGMtYmFlMS03YjJjLTkzMDktMmZhMWUwZTE5NjAzOjQ2NDAwMTI4LTUxMTUtNDEyMi1hZjEzLWY4Njc1ODM0ZDhiYg=="

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()
        self.api_key = self.db.get("GigaChat", "api_key", "")

    @loader.unrestricted
    async def gptapicmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите API-ключ: .gptapi ваш_ключ</b>")
            return
        self.api_key = args
        self.db.set("GigaChat", "api_key", args)
        await message.edit("<b>✅ API-ключ GigaChat сохранён</b>")

    @loader.unrestricted
    async def gptcmd(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            await message.edit("<b>Напишите запрос или ответьте на сообщение</b>")
            return

        if not self.api_key:
            await message.edit("<b>❌ Не установлен API-ключ. Используйте .gptapi ваш_ключ</b>")
            return

        query = args if args else reply.text

        await message.edit("<b>Выполняется by GenitzGPT...</b>")

        try:
            response = requests.post(
                "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "GigaChat:latest",
                    "messages": [{"role": "user", "content": query}]
                },
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка GigaChat: {str(e)}</b>")
            return

        result_text = f"<b>Запрос:</b> {query}\n\n<b>Ответ GigaChat:</b> {answer}"
        await message.edit(result_text, parse_mode="HTML")
