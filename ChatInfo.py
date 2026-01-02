from telethon import events
from .. import loader, utils

def register(cb):
    cb(ChatInfoMod())

class ChatInfoMod(loader.Module):
    """Модуль для отображения ID текущего чата"""
    
    strings = {"name": "ChatInfo"}

    @loader.unrestricted
    async def chatinfocmd(self, message):
        """Вывести ID текущего чата"""
        chat_id = str(message.chat_id)
        await utils.answer(message, f"<b>ID текущего чата:</b> {chat_id}")
