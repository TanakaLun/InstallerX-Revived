import asyncio
import os
import sys
from telethon import TelegramClient

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOTTOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MESSAGE_THREAD_ID = os.environ.get("MSGID")

def check_environ():
    global CHAT_ID, MESSAGE_THREAD_ID
    if BOT_TOKEN is None:
        print("[-] Invalid BOT_TOKEN")
        exit(1)

    if CHAT_ID is not None:
        try:
            CHAT_ID = int(CHAT_ID)
        except:
            pass

    if MESSAGE_THREAD_ID and MESSAGE_THREAD_ID != "":
        try:
            MESSAGE_THREAD_ID = int(MESSAGE_THREAD_ID)
        except:
            MESSAGE_THREAD_ID = None
    else:
        MESSAGE_THREAD_ID = None

async def main():
    check_environ()
    files = sys.argv[1:]
    
    if not files:
        print("[-] No files to upload")
        exit(1)

    print("[+] Logging in Telegram with bot")
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    session_dir = os.path.join(script_dir, "module_send_session")

    client = TelegramClient(session=session_dir, api_id=API_ID, api_hash=API_HASH)
    async with await client.start(bot_token=BOT_TOKEN) as bot:
        print(f"[+] Sending {len(files)} files to {CHAT_ID} (Topic: {MESSAGE_THREAD_ID})")
        
        await bot.send_file(
            entity=CHAT_ID,
            file=files,
            reply_to=MESSAGE_THREAD_ID,
            parse_mode="markdown"
        )
        print("[+] Done!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] An error occurred: {e}")
