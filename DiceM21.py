from telethon import events
from random import randint
from .. import loader, utils

@loader.module(name="Dice", author="MaximPlay")
class DiceMod(loader.Module):
    strings = {"name": "Dice"}

    @loader.command()
    async def dicecmd(self, message):
        """Бросить кости. Использование: .dice [число от 1 до 6]"""
        args = utils.get_args_raw(message)
        
        if args and args.isdigit():
            value = int(args)
            if value < 1 or value > 6:
                await utils.answer(message, '<b>❌ Некорректное значение! Допустимы только числа от 1 до 6.</b>')
                return
        else:
            value = randint(1, 6)
        
        await self.client.send_dice(message.to_id, emoji="🎲", value=value)
        await message.delete()

def register(module_name):
    """Регистрация модуля в системе"""
    return DiceMod()
