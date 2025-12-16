from telethon import events

def register(cb):
 cb(VagneraADSMod())


class VagneraADSMod(loader.Module):
    """VagneraADS By Genitz"""

    strings = {'name': 'VagneraADS'}

DEFAULT_LINK = "https://example.com"
DEFAULT_TEXT = "Нажми сюда"

@client.on(events.NewMessage(pattern=r'^\.ad\s+(.+)####REPLACEMENT_CODE_0#####39;))
async def set_default_link(event):
    new_link = event.pattern_match.group(1).strip()
    if not new_link.startswith(('http://', 'https://')):
        await event.reply("❌ Ссылка должна начинаться с http:// или https://")
        return
    global DEFAULT_LINK
    DEFAULT_LINK = new_link
    await event.reply(f"✅ Фиксированная ссылка обновлена: {DEFAULT_LINK}")

@client.on(events.NewMessage(pattern=r'^\.a\s*(.*)####REPLACEMENT_CODE_0#####39;))
async def add_link(event):
    args = event.pattern_match.group(1).strip()
    original_text = event.message.text.strip()
    if original_text.startswith('.a'):
        original_text = original_text[2:].strip()
    
    if args:
        if ' ' in args:
            parts = args.split(' ', 1)
            custom_text = parts[0]
            link = parts[1]
        else:
            link = args
            custom_text = DEFAULT_TEXT
    else:
        link = DEFAULT_LINK
        custom_text = DEFAULT_TEXT
    
    if not link.startswith(('http://', 'https://')):
        await event.reply("❌ Ссылка должна начинаться с http:// или https://")
        return
    
    clickable_link = f"{custom_text}"
    
    if not original_text:
        await event.reply(clickable_link, parse_mode='markdown')
        return
    
    new_text = original_text + "
" + clickable_link
    
    try:
        await event.edit(new_text, parse_mode='markdown')
    except:
        await event.reply(new_text, parse_mode='markdown')