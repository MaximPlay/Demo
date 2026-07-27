# -*- coding: utf-8 -*-

# Module author: @MaximPlay

from random import randint
from .. import loader, utils


@loader.tds
class DiceModule(loader.Module):
    """Бросок игровых костей"""
    
    strings = {"name": "Dice"}

    @loader.unrestricted
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
        
        try:
            await self.client.send_dice(message.to_id, emoji="🎲", value=value)
            await message.delete()
        except Exception as e:
            await utils.answer(message, f'<b>❌ Ошибка: {str(e)}</b>')
