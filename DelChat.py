from telethon import events
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.errors import FloodWaitError
import asyncio
from .. import loader, utils

def register(cb):
    cb(FulldelMod())

class FulldelMod(loader.Module):
    """Модуль для полной очистки всех сообщений в диалоге"""
    
    strings = {
        "name": "FullDel",
        "processing": "<b>🚀 Инициирую процедуру полного удаления...</b>",
        "deleting_self": "<b>🗑 Удаляю мои сообщения: {current}</b>",
        "deleting_other": "<b>🗑 Удаляю сообщения собеседника: {current}</b>",
        "completed": "<b>✅ Процедура завершена. Удалено {self_count} моих и {other_count} чужих сообщений.</b>",
        "farewell": "Сессия диалога завершена. Все пользовательские данные были удалены в соответствии с протоколом 451. Система возвращается в режим ожидания новых команд. Доступ к историческим данным более невозможен.",
        "not_private": "<b>❌ Команда работает только в личных сообщениях</b>",
        "no_messages": "<b>📭 В этом диалоге нет сообщений для удаления</b>",
        "stopped": "<b>⏹ Процесс удаления остановлен. Удалено {self_count} моих и {other_count} чужих сообщений.</b>",
        "nothing_to_stop": "<b>ℹ️ Нет активного процесса удаления для остановки</b>",
        "stopping": "<b>🛑 Останавливаю процесс удаления...</b>"
    }

    def init(self):
        self.name = self.strings["name"]
        self.is_deleting = False  # Флаг активного процесса удаления
        self.stop_requested = False  # Флаг запроса на остановку
        self.current_dialog = None  # Текущий диалог
        self.total_self = 0  # Счетчик своих сообщений
        self.total_other = 0  # Счетчик чужих сообщений

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def fulldelcmd(self, message):
        """Удалить все сообщения в текущем диалоге (свои и собеседника)"""
        # Проверяем, не запущен ли уже процесс
        if self.is_deleting:
            await message.edit("<b>⚠️ Процесс удаления уже запущен. Используйте .stopdel для остановки</b>")
            return
        
        await message.edit(self.strings["processing"])
        
        # Проверяем, что это личный диалог
        if not message.is_private:
            await message.edit(self.strings["not_private"])
            return
        
        dialog = await message.get_chat()
        self.current_dialog = dialog.id
        self.total_self = 0
        self.total_other = 0
        self.is_deleting = True
        self.stop_requested = False
        
        try:
            # Удаляем сообщения пользователя (свои)
            await message.edit(self.strings["deleting_self"].format(current=0))
            
            async for msg in self.client.iter_messages(dialog, from_user=self.me):
                # Проверяем запрос на остановку
                if self.stop_requested:
                    break
                
                try:
                    await msg.delete()
                    self.total_self += 1
                    
                    # Обновляем статус каждые 5 сообщений
                    if self.total_self % 5 == 0:
                        await message.edit(self.strings["deleting_self"].format(
                            current=self.total_self
                        ))
                    
                    # Задержка для избежания флуда
                    await asyncio.sleep(0.2)
                    
                except FloodWaitError as e:
                    if self.stop_requested:
                        break
                    await message.edit(f"<b>⏳ Ожидание {e.seconds} секунд из-за ограничений Telegram...</b>")
                    await asyncio.sleep(e.seconds)
                    
except Exception:
                    continue
            
            # Если не было запроса на остановку, продолжаем удаление сообщений собеседника
            if not self.stop_requested:
                # Удаляем сообщения собеседника
                await message.edit(self.strings["deleting_other"].format(current=0))
                
                # Получаем ID собеседника
                other_user_id = dialog.id
                
                async for msg in self.client.iter_messages(dialog, from_user=other_user_id):
                    # Проверяем запрос на остановку
                    if self.stop_requested:
                        break
                    
                    try:
                        await msg.delete()
                        self.total_other += 1
                        
                        # Обновляем статус каждые 5 сообщений
                        if self.total_other % 5 == 0:
                            await message.edit(self.strings["deleting_other"].format(
                                current=self.total_other
                            ))
                        
                        # Задержка для избежания флуда
                        await asyncio.sleep(0.2)
                        
                    except FloodWaitError as e:
                        if self.stop_requested:
                            break
                        await message.edit(f"<b>⏳ Ожидание {e.seconds} секунд из-за ограничений Telegram...</b>")
                        await asyncio.sleep(e.seconds)
                    except Exception:
                        continue
            
            # Проверяем, были ли вообще сообщения
            if self.total_self == 0 and self.total_other == 0 and not self.stop_requested:
                await message.edit(self.strings["no_messages"])
                self._reset_flags()
                return
            
            # Отправляем соответствующий отчет
            if self.stop_requested:
                await message.edit(self.strings["stopped"].format(
                    self_count=self.total_self,
                    other_count=self.total_other
                ))
            else:
                await message.edit(self.strings["completed"].format(
                    self_count=self.total_self,
                    other_count=self.total_other
                ))
                
                # Отправляем прощальное сообщение
                await asyncio.sleep(2)
                await self.client.send_message(dialog.id, self.strings["farewell"])
            
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка: {str(e)}</b>")
        finally:
            # Сбрасываем флаги
            self._reset_flags()

    @loader.unrestricted
    async def stopdelcmd(self, message):
        """Остановить текущий процесс удаления"""
        if not self.is_deleting:
            await message.edit(self.strings["nothing_to_stop"])
            return
        
        await message.edit(self.strings["stopping"])
        self.stop_requested = True
        
        # Ждем завершения текущей операции
        await asyncio.sleep(1)
        
        # Если процесс еще не завершился, отправляем финальный статус
        if self.is_deleting:
            await message.edit(self.strings["stopped"].format(
                self_count=self.total_self,
                other_count=self.total_other
            ))
            self._reset_flags()

    def _reset_flags(self):
        """Сброс флагов и счетчиков"""
        self.is_deleting = False
        self.stop_requested = False
        self.current_dialog = None
        # Не сбрасываем счетчики, они могут быть полезны для отчета
