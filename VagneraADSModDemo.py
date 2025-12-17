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
        # Поддерживаем оба типа ссылок: HTTP(S) и @username
        self.default_link = ""
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
            await message.edit("<b>Укажите ссылку: .ad https://example.com или .ad @username</b>")
            return
    
        # Определяем тип ссылки: HTTP(S) или @username
        if args.startswith("http://") or args.startswith("https://"):
            self.default_link = args
        elif args.startswith("@"):
            # Убираем символ '@' перед сохранением
            self.default_link = args.lstrip('@')
        else:
            await message.edit("<b>🚫 Неправильный формат ссылки. Используйте либо HTTP(S), либо @username.</b>")
            return
        
        await message.edit(f"<b>✅ Стандартная ссылка обновлена: {args}</b>")

    @loader.unrestricted
    async def acmd(self, message):
        """Создает кликабельную ссылку с заданным текстом"""
        args = utils.get_args_raw(message)
        custom_text = args or self.default_text
        link = self.default_link
    
        # Формируем ссылку в зависимости от её типа
        if link.startswith("http://") or link.startswith("https://"):
            clickable_link = f'<a href="{link}">{custom_text}</a>'
        else:
            # Если это username, используем tg://resolve
            clickable_link = f'<a href="tg://resolve?domain={link}">{custom_text}</a>'
        
        await message.edit(clickable_link, parse_mode="HTML")
