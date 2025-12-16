from telethon import events
from .. import loader, utils

def register(cb):
    cb(VagneraADSMod())

class VagneraADSMod(loader.Module):
    strings = {"name": "VagneraADS"}

    def [b]init[/b](self):
        self.name = self.strings["name"]
        self.me = None
        self.ratelimit = []
        self.default_link = "https://example.com"
        self.default_text = "Нажми сюда"

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = await client.get_me()

    @loader.unrestricted
    async def adcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите ссылку: .ad https://example.com</b>")
            return
        if not args.startswith(("http://", "https://")):
            await message.edit("<b>Ссылка должна начинаться с http:// или https://</b>")
            return
        self.default_link = args
        await message.edit(f"<b>✅ Ссылка по умолчанию обновлена: {args}</b>")

    @loader.unrestricted
    async def acmd(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        original_text = message.text
        if original_text.startswith(".a"):
            original_text = original_text[2:].strip()
        if not args:
            link = self.default_link
            custom_text = self.default_text
        else:
            if " " in args:
                parts = args.split(" ", 1)
                custom_text = parts[0]
                link = parts[1]
            else:
                link = args
                custom_text = self.default_text
        if not link.startswith(("http://", "https://")):
            await message.edit("<b>Ссылка должна начинаться с http:// или https://</b>")
            return
        clickable_link = f'<a href="{link}">{custom_text}</a>'
if not original_text:
    await message.edit(clickable_link, parse_mode="html")
    return
new_text = original_text + "
" + clickable_link
await message.edit(new_text, parse_mode="html")
