import psutil
import asyncio

async def handle_process_list(context, chat_id):
    procs = []
    for proc in psutil.process_iter(['pid', 'name']):
        procs.append(f"{proc.info['pid']}: {proc.info['name']}")

    chunk_size = 3000
    text = "\n".join(procs)
    for i in range(0, len(text), chunk_size):
        await context.bot.send_message(chat_id=chat_id, text=text[i:i+chunk_size])
