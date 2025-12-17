from telethon import events
from .. import loader, utils

@loader.tds
class DKSImageMod(loader.Module):
    """Отправляет изображение при команде .dks"""

    strings = {
        "name": "DKSImage",
        "image_sent": "Изображение отправлено!"
    }

    async def dks_cmd(self, message):
        """Отправляет изображение при команде .dks"""
        await message.respond(file="l-intro-1759553752.jpg")
        await message.respond(self.strings["image_sent"])
