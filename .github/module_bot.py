from telethon import TelegramClient, sessions
import asyncio
import os
import sys

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MESSAGE_THREAD_ID = os.environ.get("MESSAGE_THREAD_ID")

async def send_telegram_files(files):
    if not CHAT_ID:
        print("[-] CHAT_ID is missing")
        return


    try:
        raw_id = str(CHAT_ID).strip()
        if not raw_id.startswith("-100"):
            if raw_id.startswith("-"):
                target_chat = int(f"-100{raw_id[1:]}")
            else:
                target_chat = int(f"-100{raw_id}")
        else:
            target_chat = int(raw_id)
            
        print(f"[+] Final Target ID: {target_chat}")
    except ValueError:
        print(f"[-] Invalid CHAT_ID format: {CHAT_ID}")
        return

    topic_id = None
    if MESSAGE_THREAD_ID and str(MESSAGE_THREAD_ID).strip():
        try:
            topic_id = int(str(MESSAGE_THREAD_ID).strip())
            print(f"[+] Sending to Topic: {topic_id}")
        except ValueError:
            print("[-] Invalid MESSAGE_THREAD_ID, sending to main channel.")

    session = sessions.StringSession()

    async with TelegramClient(session, api_id=int(API_ID), api_hash=API_HASH) as client:
        await client.start(bot_token=BOT_TOKEN)
        
        try:
            entity = await client.get_input_entity(target_chat)
        except Exception as e:
            print(f"[!] Entity resolution failed, using raw ID: {e}")
            entity = target_chat

        print(f"[+] Sending {len(files)} files...")
        
        await client.send_file(
            entity=entity,
            file=files,
            reply_to=topic_id
        )
        print("[+] Files sent successfully.")

if __name__ == '__main__':
    file_list = sys.argv[1:]
    if file_list:
        try:
            asyncio.run(send_telegram_files(file_list))
        except Exception as e:
            print(f"[-] An error occurred: {e}")
    else:
        print("[-] No files provided as arguments.")
