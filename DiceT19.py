from telethon import events
from random import randint
from .. import loader, utils

class DiceModule(loader.Module):
    """Модуль для броска игральной кости"""
    strings = {"name": "Dice"}

    @loader.unrestricted
    async def dicecmd(self, message):
        """Бросает игральную кость. Опционально можно указать нужный результат.
           Пример: '.dice 3' — бросит кубик с результатом 3,
                   '.dice' — бросит случайный результат от 1 до 6."""
        
        args = utils.get_args_raw(message)
        value = int(args) if args and args.isdigit() else randint(1, 6)
        
        if value < 1 or value > 6:
            await utils.answer(message, '<b>Неверное значение. Число должно быть от 1 до 6.</b>')
            return
        
        await self.client.send_dice(message.to_id, emoji='🎲', value=value)
        await message.delete()

__version__ = "1.0.0"
__author__ = "Genitz"

async def on_load(client):
    print("Модуль Dice успешно загружен.")

async def config_complete():
    global __version__, __author__
    __module__ = "dice"
    __version__ = "1.0.0"
    __author__ = "Genitz"
