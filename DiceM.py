from telethon import events
from random import randint
from .. import loader, utils

def register(cb):
    cb(Кубик())

class DiceModule(loader.Module):
    """Кинь кубик епта (.dice [результат])"""
    
    strings = {"name": "Dice"}

    @loader.unrestricted
    async def dicecmd(self, message):
        
        
        args = utils.get_args_raw(message)
        value = int(args) if args and args.isdigit() else randint(1, 6)
         
        if value < 1 or value > 6:
            await utils.answer(message, '<b>Некорректное значение!</b>')
            return
        
        await self.client.send_dice(message.to_id, emoji="🎲", value=value)
        await message.delete()
