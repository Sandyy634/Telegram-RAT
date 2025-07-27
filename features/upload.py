import os
import asyncio

async def handle_upload(update, context):
    await update.message.reply_text("📤 Please send the file as document.")

async def handle_file_receive(update, context):
    doc = update.message.document
    if doc:
        file = await context.bot.get_file(doc.file_id)
        filename = doc.file_name
        await file.download_to_drive(custom_path=filename)
        await update.message.reply_text(f"✅ Uploaded file saved as {filename}")
