token = '1891854677:AAEDNLc4q9cbtfHMI0JoBKviVx6gFLsApb4'

from telegram import (Update, ReplyKeyboardMarkup)
from telegram.ext import Updater, dispatcher
from telegram.ext import (
    CommandHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext)
import logging

from utility.util import logger

def start(update:Update, context:CallbackContext):
    # context.bot.send_message(chat_id= update.effective_chat.id, text= "I'm a botm please talk to me !")
    update.message.reply_text("I'm a bot. hey!")
    update.message.reply_document()



def main():
    updater = Updater(token= token, use_context= True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level= logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()