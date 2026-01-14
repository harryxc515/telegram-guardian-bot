import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatPermissions

from config import *
from database import *
from lang import t
from ai_guard import *

app = Client("guardian", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_admin(m):
    return m.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)

async def log(text):
    await app.send_message(LOG_CHANNEL, text)

@app.on_message(filters.command("help") & filters.group)
async def help_cmd(_, m):
    await m.reply(t(get_lang(m.chat.id), "help"))

@app.on_message(filters.command("stats") & filters.group)
async def stats_cmd(_, m):
    s = get_stats(m.chat.id)
    await m.reply(
        f"📊 Group Stats\n"
        f"Violations: {s.get('violations',0)}\n"
        f"Spam: {s.get('spam',0)}\n"
        f"NSFW: {s.get('nsfw',0)}\n"
        f"Toxic: {s.get('toxic',0)}"
    )

@app.on_message(filters.command("whitelist") & filters.group)
async def wl_cmd(_, m):
    member = await app.get_chat_member(m.chat.id, m.from_user.id)
    if not is_admin(member):
        return
    add_whitelist(m.chat.id, m.command[1])
    await m.reply("✅ Whitelisted")

@app.on_message(filters.text & filters.group)
async def moderate(_, m):
    if m.from_user.is_bot:
        return

    wl = get_whitelist(m.chat.id)
    lang = get_lang(m.chat.id)

    if (
        has_link(m.text, wl)
        or ai_check(m.text, "spam")
        or ai_check(m.text, "nsfw")
        or ai_check(m.text, "toxic")
    ):
        strikes = add_warning(m.chat.id, m.from_user.id)
        add_stat(m.chat.id, "violations")
        await m.delete()

        await app.restrict_chat_member(
            m.chat.id,
            m.from_user.id,
            ChatPermissions(),
            until_date=int(asyncio.get_event_loop().time()) + AUTO_UNMUTE_SECONDS
        )

        await m.chat.send_message(t(lang, "muted", time=AUTO_UNMUTE_SECONDS))
        await log(f"🚨 Violation | Group:{m.chat.title} | User:{m.from_user.id}")

        if strikes >= 3:
            await app.ban_chat_member(m.chat.id, m.from_user.id)

app.run()