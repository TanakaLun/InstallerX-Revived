from telethon import TelegramClient
import asyncio
import os
import sys

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOTTOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MESSAGE_THREAD_ID = os.environ.get("MSGID")
VERSION = os.environ.get("NEW_VERSION", "Unknown")
BUILD_TIME = os.environ.get("BUILD_TIME", "Unknown")

async def main():
    files = [os.path.abspath(f) for f in sys.argv[1:] if os.path.exists(f)]
    if not files:
        return

    caption = (
        f"📦 **InstallerX Revived Build**\n"
        f"{"—"*20}\n"
        f"✨ **Version:** `{VERSION}`\n"
        f"📅 **Build Time:** `{BUILD_TIME}`\n"
        f"🛠 **Status:** `#Unstable #Preview`\n"
        f"{"—"*20}\n"
        f"🔗 [Upstream Repository]({os.environ.get('UPSTREAM_REPO')})"
    )
    
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    session_dir = os.path.join(script_dir, "module_send_session")
    client = TelegramClient(session=session_dir, api_id=API_ID, api_hash=API_HASH)
    
    async with await client.start(bot_token=BOT_TOKEN) as bot:
        await bot.send_file(
            entity=int(CHAT_ID),
            file=files,
            caption=caption,
            reply_to=int(MESSAGE_THREAD_ID) if MESSAGE_THREAD_ID else None,
            parse_mode="markdown"
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        pass
