from telethon import events
from .. import loader, utils

def register(cb):
    cb(VagneraADSMod())

class VagneraADSMod(loader.Module):
    strings = {"name": "VagneraADS"}

    def __init__(self):
        self.name = self.strings["name"]
        self.me = None
        self.ratelimit = []
        # Добавляем поддержку ссылок формата @username
        self.default_link = "@rmcfnew3"
        self.default_text = "Нажми сюда"

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def adcmd(self, message):
        """Обновляет стандартную ссылку"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите ссылку: .ad @rmcfnew3</b>")
            return
        
        # Проверяем, начинается ли ссылка с символа '@'
        if not args.startswith("@"):
            await message.edit("<b>🚫 Ссылка должна начинаться с символа @</b>")
            return
            
        self.default_link = args
        await message.edit(f"<b>✅ Стандартная ссылка обновлена: {args}</b>")

    @loader.unrestricted
    async def acmd(self, message):
        """Создает кликабельную ссылку с заданным текстом"""
        args = utils.get_args_raw(message)
        custom_text = args or self.default_text
        link = self.default_link
        clickable_link = f'<a href="tg://resolve?domain={link}">{custom_text}</a>'
        await message.edit(clickable_link, parse_mode="HTML")
