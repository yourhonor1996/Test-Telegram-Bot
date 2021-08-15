import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level= logging.INFO)
import os
from django import setup
from functools import wraps                        

def logger(message:str, *args, **kwargs):
    return logging.log(logging.INFO, message, *args, **kwargs)

from telegram import ChatAction, Update
from telegram.ext import CallbackContext



class classproperty(object):
    '''Converts a class method into a class property. However this property cannot be set it can only be called.'''
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
    
  
def config_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botdjango.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    setup()  


# extract chat_id based on the incoming object
def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id

def resolve_text_md(text:str):
    '''resolves the text for markdown doing these:
        - replaces .  with \.'''
    return text.replace('.', '\\.')


def send_typing_action(func):
    """Sends typing action while processing func command."""
    
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

def get_update(update:Update, context:CallbackContext):
    '''get the update based on whether it is a callback_query or a regular update.
    if the callback_query doesn't exits it will return a regular update'''
    if not update.callback_query:
        return update
    return update.callback_query


def get_session_question_ids(session):
    # we have to import django models after the settings configuratoin. We can't import models in the global scope.
    from src import models
    return models.SessionQuestion.objects.filter(session= session).order_by('id').values_list('id', flat= True)