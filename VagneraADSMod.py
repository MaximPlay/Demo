from telethon import events

DEFAULT_LINK = "https://example.com"
DEFAULT_TEXT = "Нажми сюда"

# Обработчик команды изменения фиксированной ссылки (.ad)
@client.on(events.NewMessage(pattern=r'^\.ad\s+(.*)$'))
async def set_default_link(event):
    new_link = event.pattern_match.group(1).strip()
    # Проверяем валидность ссылки
    if not new_link.startswith(('http://', 'https://')):
        await event.reply("❌ Ссылка должна начинаться с http:// или https://")
        return
    # Обновляем глобальную переменную с дефолтной ссылкой
    global DEFAULT_LINK
    DEFAULT_LINK = new_link
    await event.reply(f"✅ Фиксированная ссылка обновлена: {DEFAULT_LINK}")

# Обработчик добавления кликабельной ссылки (.a)
@client.on(events.NewMessage(pattern=r'^\.a\s*(.*)$'))
async def add_link(event):
    args = event.pattern_match.group(1).strip()  # Получаем аргументы команды
    text = event.message.text.strip()  # Исходный текст сообщения
    
    # Если сообщение начинается с .a, очищаем команду
    if text.startswith('.a'):
        text = text[2:].strip()
        
    # Определяем ссылку и текст кнопки
    if args:
        if ' ' in args:
            parts = args.split(maxsplit=1)
            custom_text = parts[0]
            link = parts[1]
        else:
            link = args
            custom_text = DEFAULT_TEXT
    else:
        link = DEFAULT_LINK
        custom_text = DEFAULT_TEXT
    
    # Проверяем валидность ссылки
    if not link.startswith(('http://', 'https://')):
        await event.reply("❌ Ссылка должна начинаться с http:// или https://")
        return
    
    # Формируем кликабельную ссылку
    clickable_link = f"[{custom_text}]({link})"
    
    # Редактируем исходное сообщение или отправляем новое
    if not text:
        await event.reply(clickable_link, parse_mode='markdown')
    else:
        new_text = text + "\n\n" + clickable_link
        try:
            await event.edit(new_text, parse_mode='markdown')
        except Exception as e:
            print(e)
            await event.reply(new_text, parse_mode='markdown')
