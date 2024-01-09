## Packages 에서 python-telegram-bot install
import telegram
import asyncio


bot = telegram.bot(token = "xxxx")
chat_id = "xxxx"

asyncio.run(bot.sendMessage(chat_id=chat_id, text = "파이선 Telegram test"))