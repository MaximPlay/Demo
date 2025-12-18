from telethon import events
from telethon.tl.types import MessageMediaDocument
from .. import loader, utils
import os

@loader.tds
class WebmStickerMod(loader.Module):
    """Загружает стикеры в формате .webm при ответе на них"""

    strings = {
        "name": "WebmSticker",
        "sticker_downloaded": "Стикер успешно загружен в формате .webm!",
        "multiple_stickers_downloaded": "Все стикеры успешно загружены в формате .webm!",
        "no_stickers": "Ответьте на стикеры, чтобы загрузить их в формате .webm."
    }

    async def webmsticker_cmd(self, message):
        """Загружает стикеры в формате .webm при ответе на них"""
        reply = await message.get_reply_message()
        if not reply or not isinstance(reply.media, MessageMediaDocument):
            await message.respond(self.strings["no_stickers"])
            return

        # Проверяем, что это стикер
        if not reply.media.document.attributes[0].sticker:
            await message.respond(self.strings["no_stickers"])
            return

        # Получаем список стикеров
        stickers = []
        async for msg in message.client.iter_messages(reply.chat_id, limit=100):
            if msg.media and isinstance(msg.media, MessageMediaDocument) and msg.media.document.attributes[0].sticker:
                stickers.append(msg)

        # Загружаем стикеры
        downloaded = []
        for i, sticker_msg in enumerate(stickers):
            sticker = await sticker_msg.download_media(file=f"sticker_{i}.webm")
            if sticker:
                downloaded.append(sticker)

        if downloaded:
            await message.respond(self.strings["multiple_stickers_downloaded"])
        else:
            await message.respond("Не удалось загрузить стикеры.")
