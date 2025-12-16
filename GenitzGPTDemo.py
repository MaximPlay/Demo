from telethon import events
from .. import loader, utils
import asyncio
import aiohttp
import ssl
import tempfile
import os

# Постоянный API-ключ (зафиксировано в коде)
API_KEY = "MDE5YjI2MGMtYmFlMS03YjJjLTkzMDktMmZhMWUwZTE5NjAzOjFiZjBlODEwLTU0YWMtNDg3Ni05NWI2LTllNjEyYWU1OTc3NA"
ROOT_CERT_URL = "https://raw.githubusercontent.com/MaximPlay/certs/refs/heads/main/russian_trusted_root_ca.cer"
INTERMEDIATE_CERT_URL = "https://raw.githubusercontent.com/MaximPlay/certs/refs/heads/main/russian_trusted_root_ca_gost_20225.cer"

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
            # Скачиваем сертификаты из репозитория
            async with aiohttp.ClientSession() as session:
                root_cert_resp = await session.get(ROOT_CERT_URL)
                intermediate_cert_resp = await session.get(INTERMEDIATE_CERT_URL)

                root_cert = await root_cert_resp.text()
                intermediate_cert = await intermediate_cert_resp.text()

            # Создаем временный файл с объединенными сертификатами
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file.write(root_cert + '\n' + intermediate_cert)
                temp_path = temp_file.name

            # Создаем SSL контекст с временным файлом
            ctx = ssl.create_default_context(cafile=temp_path)

            # Делаем запрос к API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={"model": "GigaChat:latest", "messages": [{"role": "user", "content": "ping"}]},
                        ssl=ctx
                ) as response:
                    response.raise_for_status()
                    await message.edit("<b>✅ API GigaChat доступен и работает нормально.</b>")
        finally:
            # Удаляем временный файл
            os.remove(temp_path)
        except aiohttp.ClientResponseError as err:
            await message.edit(f"<b>❌ Ошибка GigaChat ({err.status}): {err.message}</b>")
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
            # Скачиваем сертификаты из репозитория
            async with aiohttp.ClientSession() as session:
                root_cert_resp = await session.get(ROOT_CERT_URL)
                intermediate_cert_resp = await session.get(INTERMEDIATE_CERT_URL)

                root_cert = await root_cert_resp.text()
                intermediate_cert = await intermediate_cert_resp.text()

            # Создаем временный файл с объединенными сертификатами
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file.write(root_cert + '\n' + intermediate_cert)
                temp_path = temp_file.name

            # Создаем SSL контекст с временным файлом
            ctx = ssl.create_default_context(cafile=temp_path)

            # Делаем запрос к API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "GigaChat:latest",
                            "messages": [{"role": "user", "content": query}]
                        },
                        ssl=ctx
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    answer = result["choices"][0]["message"]["content"]
        finally:
            # Удаляем временный файл
            os.remove(temp_path)
        except aiohttp.ClientResponseError as err:
            await message.edit(f"<b>❌ Ошибка GigaChat ({err.status}): {err.message}</b>")
            return
        except Exception as e:
            await message.edit(f"<b>❌ Произошла ошибка: {str(e)}</b>")
            return

        result_text = f"<b>Запрос:</b> {query}\n\n<b>Ответ GigaChat:</b> {answer}"
        await message.edit(result_text, parse_mode="HTML")
