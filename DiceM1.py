from telethon import events
from random import randint
from .. import loader, utils

def register(cb):
    cb(DiceModule())

class DiceModule(loader.Module):
    strings = {"name": "Dice"}

    @loader.unrestricted
    async def dicecmd(self, message):
        args = utils.get_args_raw(message)
        
        if args and args.isdigit():
            value = int(args)
            if value < 1 or value > 6:
                await utils.answer(message, '<b>Некорректное значение! Допустимы только числа от 1 до 6.</b>')
                return
        else:
            value = randint(1, 6)
        
        await self.client.send_dice(message.to_id, emoji="🎲", value=value)
        await message.delete()
