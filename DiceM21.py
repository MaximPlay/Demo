#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from random import randint

from .. import loader, utils, security

logger = logging.getLogger(__name__)


@loader.tds
class DiceMod(loader.Module):
    """Бросок игровых костей"""
    strings = {"name": "Dice"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "POSSIBLE_VALUES", 
            {
                "🎲": [1, 2, 3, 4, 5, 6],
                "🎯": [1, 2, 3, 4, 5, 6],
                "🏀": [1, 2, 3, 4, 5]
            },
            "Доступные значения для разных эмодзи"
        )

    @loader.unrestricted
    async def dicecmd(self, message):
        """Бросить кости.
           Использование: .dice [эмодзи] [значение]
           Пример: .dice 🎲 5"""
        args = utils.get_args(message)
        
        # Определяем эмодзи
        if args and args[0] in ["🎲", "🎯", "🏀"]:
            emoji = args[0]
            args = args[1:]  # Убираем эмодзи из аргументов
        else:
            emoji = "🎲"
        
        # Получаем возможные значения для эмодзи
        possible_values = self.config["POSSIBLE_VALUES"].get(emoji, [1, 2, 3, 4, 5, 6])
        
        # Определяем значение
        if args and args[0].isdigit():
            value = int(args[0])
            if value not in possible_values:
                await utils.answer(message, 
                    f'<b>❌ Некорректное значение! Для {emoji} допустимы: {", ".join(map(str, possible_values))}</b>')
                return
        else:
            value = randint(1, 6)
            # Корректируем значение если оно не подходит для эмодзи
            if value not in possible_values:
                value = possible_values[randint(0, len(possible_values) - 1)]
        
        try:
            # Отправляем кубик с нужным значением
            await self.client.send_dice(message.to_id, emoji=emoji, value=value)
            await message.delete()
        except Exception as e:
            await utils.answer(message, f'<b>❌ Ошибка: {str(e)}</b>')
