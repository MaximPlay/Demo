from telethon import events, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from .. import loader, utils

def register(cb):
    cb(ExtendedChatInfoMod())

class ExtendedChatInfoMod(loader.Module):
    """Расширенный модуль для отображения подробной информации о чате"""
    
    strings = {"name": "ExtendedChatInfo"}

    @loader.unrestricted
    async def chatinfocmd(self, message):
        """Показать подробную информацию о текущем чате."""
        chat = await message.get_chat()
        chat_full = None
        if isinstance(chat, events.NewMessage.Event):
            if isinstance(chat, types.Chat):
                chat_full = await self.client(GetFullChatRequest(chat.id))
            elif isinstance(chat, types.Channel):
                chat_full = await self.client(GetFullChannelRequest(chat.id))

        info_list = [
            f"<b>🔍 Информация о чате:</b>\n\n",
            f"- <b>ID чата:</b> {message.chat_id}",
            f"- <b>Название:</b> {getattr(chat, 'title', 'нет')}",
            f"- <b>Тип:</b> {'Группа' if isinstance(chat, types.Chat) else ('Канал' if isinstance(chat, types.Channel) else 'Частный чат')} ",
            f"- <b>Участники:</b> {getattr(chat_full.full_chat, 'participants_count', 'не известно')}" if chat_full else "- Участники: не известны",
            f"- <b>Описание:</b> {getattr(chat_full.full_chat, 'about', '')}" if chat_full else "",
            f"- <b>Создан:</b> {getattr(chat, 'date', '-')}",
            f"- <b>Последнее изменение:</b> {getattr(chat, 'edit_date', '-')}",
            f"- <b>Открытый доступ:</b> {'Да' if getattr(chat, 'public', False) else 'Нет'}",  # Исправленная строка
            f"- <b>Приглашающая ссылка:</b> {getattr(chat_full.full_chat, 'invite', 'нет')}" if chat_full else ""
        ]

        # Отфильтруем пустые строки
        info_list = list(filter(lambda x: len(x.strip()) > 0, info_list))

        # Объединение списка в единый ответ
        result = "\n".join(info_list)
        await utils.answer(message, result)
