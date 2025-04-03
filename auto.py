task = None

@events.register(events.NewMessage(pattern=r'\.autol (\d+) (.+)'))
async def autol_handler(event):
    global task
    if task:
        await event.respond("Уже выполняется задача. Остановите её перед запуском новой.")
        return

    # Извлечение интервала и текста из команды
    interval_minutes = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)

    # Функция для отправки сообщений
    async def send_messages():
        while True:
            await event.client(SendMessageRequest(event.chat_id, text))
            await asyncio.sleep(interval_minutes * 60)

    # Запуск задачи
    task = asyncio.create_task(send_messages())
    await event.respond(f"Автоматическая отправка сообщений начата с интервалом {interval_minutes} минут.")

@events.register(events.NewMessage(pattern=r'\.alstop'))
async def alstop_handler(event):
    global task
    if task:
        task.cancel()
        task = None
        await event.respond("Автоматическая отправка сообщений остановлена.")
    else:
        await event.respond("Нет активной задачи для остановки.")

# Регистрация обработчиков
def register_handlers(client):
    client.add_event_handler(autol_handler)
    client.add_event_handler(alstop_handler)
