token = '1891854677:AAGdDC2MEkq-EQOvwuiIdqz9Kn94xOUFHBI'
from src.utility.util import config_django
config_django()

from telegram import (Update, ReplyKeyboardMarkup)
from telegram.ext import Updater, dispatcher
from telegram.ext import (
    CommandHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext)
import logging
from src.utility.util import logger
from src import models
from django.conf import settings



def start(update:Update, context:CallbackContext):
    # context.bot.send_message(chat_id= update.effective_chat.id, text= "I'm a botm please talk to me !")
    update.message.reply_text("I'm a bot. hey!")


def subject_select(update:Update, context:CallbackContext):
    ''' Select a subject from the given subjects.'''
    resutls = models.Question.objects.select_random(5).values_list('id', flat= True)
    update.message.reply_text(str(resutls))
    



def main():
    
    updater = Updater(token= token, use_context= True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level= logging.INFO)

    start_handler = CommandHandler('start', start)
    start_handler2 = CommandHandler('comm', subject_select)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(start_handler2)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()