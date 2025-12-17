from telethon import Button
from telethon.events import CallbackQuery, NewMessage
from telethon.utils import get_display_name
from .. import loader, utils

@loader.tds
class QuizBotMod(loader.Module):
    """Интерактивный бот для создания и прохождения быстрых викторин с использованием UI-кнопок."""

    strings = {
        "name": "QuizBot",
        "start_quiz": "🎯 Начнем викторину?",
        "choose_category": "Выберите категорию викторины:",
        "ask_question": "Ваш вопрос для викторины:",
        "add_options": "Варианты ответов через запятую:",
        "poll_running": "Викторина запущена! Голосуйте ниже ⬇️",
        "results": "\n🔥 Итоги викторины:\n{}",
        "finish_poll": "Викторина завершена!"
    }

    async def on_load(self):
        self.quizzes = {}  # Хранение активных викторин

    async def quiz_start_cmd(self, event):
        """Запустите новую викторину с выбором категории"""
        await event.respond(self.strings["start_quiz"], buttons=[
            Button.inline('История', b'history'),
            Button.inline('География', b'geography'),
            Button.inline('Литература', b'literature'),
            Button.inline('Моя тема', b'custom')
        ])

    async def quiz_callback_handler(self, event):
        """Обрабатываем выбор категории и запускаем следующий этап"""
        category = event.data.decode().lower()
        chat_id = event.chat_id
        self.quizzes[chat_id] = {'category': category}
        await event.respond(self.strings["ask_question"])

    async def quiz_question_handler(self, event):
        """Собираем вопрос викторины"""
        question = event.text.strip()
        chat_id = event.chat_id
        self.quizzes[chat_id]['question'] = question
        await event.respond(self.strings["add_options"])

    async def quiz_options_handler(self, event):
        """Собираем варианты ответов"""
        options = event.text.split(',')
        chat_id = event.chat_id
        self.quizzes[chat_id]['options'] = options
        poll_buttons = [
            Button.inline(opt.strip(), bytes(str(i), encoding='utf-8')) 
            for i, opt in enumerate(options)
        ]
        await event.respond(self.quizzes[chat_id]['question'], buttons=poll_buttons)

    async def quiz_vote_handler(self, event):
        """Обрабатываем голос участников викторины"""
        index = int(event.data.decode())
        chat_id = event.chat_id
        votes = self.quizzes.get(chat_id, {}).get('votes', {})
        votes[index] = votes.get(index, 0) + 1
        self.quizzes[chat_id]['votes'] = votes
        await event.answer(self.strings["poll_running"])

    async def quiz_results_cmd(self, event):
        """Показываем результаты викторины"""
        chat_id = event.chat_id
        results = self.quizzes.get(chat_id, {}).get('votes', {})
        result_str = '\n'.join([f"{opt}: {cnt}" for opt, cnt in zip(self.quizzes[chat_id]['options'], results.values())])
        await event.respond(self.strings["results"].format(result_str))

    async def finish_quiz_cmd(self, event):
        """Заканчиваем викторину и показываем итоги"""
        chat_id = event.chat_id
        del self.quizzes[chat_id]
        await event.respond(self.strings["finish_poll"])
