from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import os
from dotenv import load_dotenv
from Drivers_admin import Driver

path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(path):
    load_dotenv(path)
TOKEN = os.environ.get('TOKEN')
URL = os.environ.get('URL')
ADMINS = os.environ.get('ADMIN')

driver = Driver(URL, ADMINS)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", driver.game_basic.start))
    dp.add_handler(CommandHandler("go", driver.game_basic.go))
    dp.add_handler(CommandHandler("prob", driver.prob))
    dp.add_handler(CommandHandler("save", driver.save))
    dp.add_handler(CommandHandler("get", driver.get))
    dp.add_handler(CommandHandler("info", driver.info))
    dp.add_handler(CommandHandler("clear", driver.clear))
    dp.add_handler(CommandHandler("yes", driver.game_basic.yes))
    dp.add_handler(CommandHandler("no", driver.game_basic.no))
    dp.add_handler(CommandHandler("end", driver.game_basic.end))
    dp.add_handler(CommandHandler("record", driver.game_basic.record))
    dp.add_handler(MessageHandler(Filters.text, driver.game_basic.text_handler))
    updater.start_polling()
    updater.idle()


main()
