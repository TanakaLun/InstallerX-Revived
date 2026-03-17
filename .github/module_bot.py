import asyncio
import os
import sys
import json
from telegram import Bot, InputMediaDocument
from telegram.constants import ParseMode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MESSAGE_THREAD_ID = os.environ.get("MESSAGE_THREAD_ID")
RUN_URL = os.environ.get("RUN_URL")
VERSION_NAME = os.environ.get("VERSION_NAME") # yy.MM.sha
VERSION_CODE = os.environ.get("VERSION_CODE") # git count
UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO")

def get_commit_info():
    try:
        with open(os.environ.get("GITHUB_EVENT_PATH"), "r") as f:
            event = json.load(f)
        if 'commits' in event:
            commits = event['commits']
            msg = "\n".join([f"• {c['message'].splitlines()[0]} by {c['author']['username']}" for c in commits[-5:]])
            return msg if msg else "No commit message"
        elif 'head_commit' in event:
            return event['head_commit']['message'].splitlines()[0]
    except:
        pass
    return "Manual build or unknown commit"

def get_caption():
    commit_msg = get_commit_info()
    return (
        f"<b>📦 InstallerX Revived Build</b>\n"
        f"————————————————————\n"
        f"✨ <b>Version:</b> <code>{VERSION_NAME}</code>\n"
        f"🔢 <b>Build:</b> <code>{VERSION_CODE}</code>\n"
        f"🛠 <b>Status:</b> #Unstable #Preview\n"
        f"————————————————————\n"
        f"📝 <b>Recent Commits:</b>\n"
        f"<pre>{commit_msg}</pre>\n"
        f"————————————————————\n"
        f"🔗 <a href='{UPSTREAM_REPO}'>Upstream</a> | <a href='{RUN_URL}'>Workflow</a>"
    )

async def main():
    if not BOT_TOKEN or not CHAT_ID:
        return
    
    files = sys.argv[1:]
    if not files:
        return

    bot = Bot(token=BOT_TOKEN)
    caption = get_caption()
    
    media_group = []
    for i, file_path in enumerate(files):
        if not os.path.exists(file_path):
            continue
        is_last = (i == len(files) - 1)
        media_group.append(InputMediaDocument(
            media=open(file_path, "rb"),
            filename=os.path.basename(file_path),
            caption=caption if is_last else None,
            parse_mode=ParseMode.HTML
        ))

    if media_group:
        await bot.send_media_group(
            chat_id=int(CHAT_ID),
            media=media_group,
            message_thread_id=int(MESSAGE_THREAD_ID) if MESSAGE_THREAD_ID else None,
            connect_timeout=60,
            write_timeout=120
        )

if __name__ == "__main__":
    asyncio.run(main())
