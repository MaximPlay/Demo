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
        self.default_link = "https://example.com"
        self.default_text = "Нажми сюда"

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def adcmd(self, message):
        """Установить новую ссылку по умолчанию"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите ссылку: .ad https://example.com</b>")
            return
            
        # Проверка корректности ссылки только при установке по умолчанию
        if not args.startswith(("http://", "https://")):
            await message.edit("<b>🚫 Ссылка должна начинаться с http:// или https://</b>")
            return
            
        # Устанавливаем ссылку по умолчанию
        self.default_link = args
        await message.edit(f"<b>✅ Ссылка по умолчанию обновлена: {args}</b>")

    @loader.unrestricted
    async def acmd(self, message):
        """Создать кликабельную ссылку с указанным текстом"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        original_text = message.text
        if original_text.startswith(".a"):
            original_text = original_text[2:].strip()
            
        # Аргумент команды .a должен стать текстом ссылки
        custom_text = args
        
        # Использовать заранее заданную ссылку по умолчанию
        link = self.default_link
        
        # Генерируем HTML-ссылку
        clickable_link = f'<a href="{link}">{custom_text}</a>'
        
        # Если изначально не было текста, показываем только ссылку
        if not original_text:
            await message.edit(clickable_link, parse_mode="HTML")
            return
        new_text = original_text + "\n" + clickable_link
        await message.edit(new_text, parse_mode="HTML")
