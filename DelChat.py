from telethon import events
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.errors import FloodWaitError
import asyncio
from .. import loader, utils

def register(cb):
    cb(FulldelMod())

class FulldelMod(loader.Module):
    """Модуль для полной очистки личных сообщений в диалоге"""
    
    strings = {
        "name": "FullDel",
        "processing": "<b>🚀 Инициирую процедуру полного удаления...</b>",
        "deleting": "<b>🗑 Удаляю сообщения: {current}/{total}</b>",
        "completed": "<b>✅ Процедура завершена. Удалено {count} сообщений.</b>",
        "farewell": "Сессия диалога завершена. Все пользовательские данные были удалены в соответствии с протоколом 451. Система возвращается в режим ожидания новых команд. Доступ к историческим данным более невозможен."
    }

    def init(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def fulldelcmd(self, message):
        """Удалить все ваши сообщения в текущем диалоге"""
        await message.edit(self.strings["processing"])
        
        # Определяем диалог
        if message.is_private:
            dialog = await message.get_chat()
        else:
            await message.edit("<b>❌ Команда работает только в личных сообщениях</b>")
            return
        
        # Получаем все сообщения пользователя в этом диалоге
        total_deleted = 0
        try:
            async for msg in self.client.iter_messages(dialog, from_user=self.me):
                try:
                    await msg.delete()
                    total_deleted += 1
                    
                    # Обновляем статус каждые 10 сообщений
                    if total_deleted % 10 == 0:
                        await message.edit(self.strings["deleting"].format(
                            current=total_deleted,
                            total="..."
                        ))
                    
                    # Небольшая задержка для избежания флуда
                    await asyncio.sleep(0.1)
                    
                except FloodWaitError as e:
                    await message.edit(f"<b>⏳ Ожидание {e.seconds} секунд из-за ограничений Telegram...</b>")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    continue
            
            # Отправляем финальные сообщения
            await message.edit(self.strings["completed"].format(count=total_deleted))
            await asyncio.sleep(2)
            await self.client.send_message(dialog, self.strings["farewell"])
            
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка: {str(e)}</b>")
