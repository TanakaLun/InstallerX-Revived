from telethon import TelegramClient, sessions
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
        print("[-] No files to upload")
        return

    caption = (
        f"✅ **Build Completed**\n\n"
        f"📱 **Module:** InstallerX Revived\n"
        f"🔢 **Version:** `{VERSION}`\n"
        f"⏰ **Time:** `{BUILD_TIME}`\n\n"
        f"#Module #Update"
    )

    print(f"[+] Logging in and sending {len(files)} files...")
    
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
        print("[+] Success!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] Error: {e}")
