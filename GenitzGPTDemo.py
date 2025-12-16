from telethon import events
from .. import loader, utils
import asyncio
import requests
import ssl
import os

# Постоянный API-ключ (зафиксировано в коде)
API_KEY = "MDE5YjI2MGMtYmFlMS03YjJjLTkzMDktMmZhMWUwZTE5NjAzOjFiZjBlODEwLTU0YWMtNDg3Ni05NWI2LTllNjEyYWU1OTc3NA=="

# Путь к объединенному сертификату (указывайте абсолютный или относительный путь)
COMBINED_CERT_PATH = 'certif.pem'  # Замените на фактический путь к объединенному сертификату

def register(cb):
    cb(GigaChatMod())

class GigaChatMod(loader.Module):
    strings = {"name": "GigaChat"}

    def __init__(self):
        self.name = self.strings["name"]
        self.me = None
        self.ratelimit = []

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def gptcfgcmd(self, message):
        """
        Проверяет доступность API GigaChat.
        """
        try:
            ctx = ssl.create_default_context(cafile=COMBINED_CERT_PATH)  # Используем объединенный сертификат
            response = requests.post(
                "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"model": "GigaChat:latest", "messages": [{"role": "user", "content": "ping"}]},
                verify=ctx  # Используем наш SSL контекст
            )
            response.raise_for_status()
            await message.edit("<b>✅ API GigaChat доступен и работает нормально.</b>")
        except requests.HTTPError as err:
            await message.edit(f"<b>❌ Ошибка GigaChat ({err.response.status_code}): {err.response.reason}</b>")
        except Exception as e:
            await message.edit(f"<b>❌ Произошла ошибка: {str(e)}</b>")

    @loader.unrestricted
    async def gptcmd(self, message):
        """
        Основной запрос к GigaChat.
        """
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            await message.edit("<b>Напишите запрос или ответьте на сообщение</b>")
            return

        query = args if args else reply.text

        await message.edit("<b>Выполняется by GenitzGPT...</b>")

        try:
            ctx = ssl.create_default_context(cafile=COMBINED_CERT_PATH)  # Используем объединенный сертификат
            response = requests.post(
                "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "GigaChat:latest",
                    "messages": [{"role": "user", "content": query}]
                },
                verify=ctx  # Используем наш SSL контекст
            )
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
        except requests.HTTPError as err:
            await message.edit(f"<b>❌ Ошибка GigaChat ({err.response.status_code}): {err.response.reason}</b>")
            return
        except Exception as e:
            await message.edit(f"<b>❌ Произошла ошибка: {str(e)}</b>")
            return

        result_text = f"<b>Запрос:</b> {query}\n\n<b>Ответ GigaChat:</b> {answer}"
        await message.edit(result_text, parse_mode="HTML")
