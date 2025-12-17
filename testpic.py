from telethon import events
from .. import loader, utils

@loader.tds
class DKSImageMod(loader.Module):
    """Отправляет изображение при команде .dks"""

    strings = {
        "name": "DKSImage",
        "image_sent": "Изображение отправлено!"
    }

    @loader.unrestricted
    async def dkscmd(self, message):
        """Отправляет изображение при команде .dks"""
        await message.respond(file="https://iimg.su/i/44099D")
        await message.respond(self.strings["image_sent"])
