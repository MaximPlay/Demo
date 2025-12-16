from telethon import events
from .. import loader, utils
import aiohttp
import json

API_URL = "https://api.gigachat.ai/v1/models/gigachat-general/inferences"

def register(cb):
    cb(GigaChatModule())  # Стандартная регистрация модуля

class GigaChatModule(loader.Module):
    strings = {"name": "GenitzGPT"}

    def __init__(self):
        self.name = self.strings["name"]
        self.me = None
        self.ratelimit = []
        self.api_key = None

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.owner
    async def gptapicmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>❗ Укажите API ключ.</b>")
            return
        self.api_key = args
        await message.edit("<b>✅ API ключ успешно установлен.</b>")

    @loader.owner
    async def gptcmd(self, message):
        reply_to_msg = await message.get_reply_message()
        input_query = utils.get_args_raw(message)
        if reply_to_msg:
            input_query = reply_to_msg.raw_text
        elif not input_query:
            await message.edit("<b>❗ Укажите запрос или ответьте на сообщение.</b>")
            return
        await message.edit("<i>Выполняется by GenitzGPT...</i>")
        payload = {
            "messages": [
                {"role": "user", "content": input_query}
            ]
        }
        HEADERS = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=HEADERS, data=json.dumps(payload)) as response:
                res_data = await response.json()
                chat_answer = res_data['choices'][0]['message']['content']
        await message.edit(f"Запрос: {input_query}\n\nОтвет GigaChat:\n{chat_answer}", parse_mode="Markdown")
