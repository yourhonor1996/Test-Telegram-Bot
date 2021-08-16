# TODO optimize regex handling in the conversations and cerate data dictionaries for them

from telegram.constants import PARSEMODE_HTML
# first we have to config django settings so we can use the ORM Module.
from src.utility.util import config_django
config_django()

from telegram import (Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from telegram.ext import Updater
from telegram.ext import (
    CommandHandler,CallbackQueryHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

import logging
from src.utility.util import logger
from src import models
from src.config import settings
from src.utility import util
from django.utils import timezone
import re


# create_quiz states
SUBJECT_SELECT, QUESTION_SELECT, TEST_CREATION = CREATE_TEST_STATES = range(3)
# quiz states
QUIZ, RESULTS = MAIN_PHASES = range(len(CREATE_TEST_STATES), len(CREATE_TEST_STATES) + 2)
# registry states
REG_CONTACT, REG_EDUCATION= REG_PHASES = range(len(MAIN_PHASES), len(MAIN_PHASES)+2)

main_keyboard = ReplyKeyboardMarkup(
        [['/start', '/register'],
        ['/create_quiz', '/start_quiz']],
        one_time_keyboard= True)

def start(update:Update, context:CallbackContext):
    message = \
    "Hello this is a quiz telegram bot. Here are the commands:\n" \
    "If you haven't registered you can register via /register" \
    "You can create a test and share it with your firends via /create_quiz\n" \
    "You can start a quiz via /start_quiz"
    
    update.message.reply_text(message, parse_mode= PARSEMODE_HTML, reply_markup= main_keyboard)

@util.send_typing_action
def cancel(update:Update, context:CallbackContext):
    this_udpate = util.get_update(update, context)
    this_udpate.message.reply_text("Canceled the process.", reply_markup= ReplyKeyboardRemove())
    return ConversationHandler.END
    
# ---------------------------------------------------------------------------------------
# Create Test Converstation

@util.send_typing_action
def create_quiz(update:Update, context:CallbackContext):
    user_id = update.message.from_user.id
    try:
        models.User.objects.get(user_id= user_id)
    except models.User.DoesNotExist:
        update.message.reply_text("You have not registered. Please register first by running the command /register")
        return ConversationHandler.END
    keyboard = [[InlineKeyboardButton("Start", callback_data= "subject_select")],
                [InlineKeyboardButton("Cancel", callback_data= "cancellqef")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Press to create the quiz: ", reply_markup=reply_markup)

    return SUBJECT_SELECT

@util.send_typing_action
def subject_select(update:Update, context:CallbackContext):
    query = update.callback_query
    # TODO make the subjects appear in two columns
    subjects = models.Subject.objects.all().values_list('id', 'name')
    keyboard = [[InlineKeyboardButton("Cancel", callback_data= "cancel")]]
    for id, name in subjects:
        keyboard.append([InlineKeyboardButton(f'{name}', callback_data= f'SUBID-{id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(text= 'Please choose the subject:', reply_markup=reply_markup)
    return QUESTION_SELECT


util.send_typing_action
def question_select(update:Update, context:CallbackContext):
    # get initial data
    now = timezone.now()
    query = update.callback_query
    from_user = query.from_user
    user_id = from_user.id
    user = models.User.objects.get(user_id= user_id)
    subject_id = int(query.data.split("-")[1])
    # get random questions
    questions_queryset = \
        models.Question.objects.select_random(settings.NUMBER_OF_QUESTIONS, subject_id).\
        filter(subject= subject_id).\
        values_list('id', flat= True)
    questions_list = list(questions_queryset)

    logger(f"List of questions: {questions_list}")
    
    # create a quiz and a session
    quiz = models.Quiz.objects.create(title= "Quiz")
    session = models.Session.objects.create(
        quiz= quiz,
        date_created= now)
    session.user.set([user])
    # create questions for this session 
    for question in questions_list:
        question_model = models.Question.objects.get(id= question)
        session_question = models.SessionQuestion.objects.create(
            session= session,
            quiz= quiz,
            question= question_model,
            date_created= now
        )

    logger(f"Session created with id <{session.id}>. Creation Date: {session.date_created}")

    # keyboard = [[InlineKeyboardButton("Start Test", callback_data= f'SESSIONID-{session.id}')],
    #             [InlineKeyboardButton("Cancel", callback_data= "cancel")]]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    subject = models.Subject.objects.get(id= subject_id)
    query.message.edit_text(
        f"You have chosen {subject.name}. Your quiz has {settings.NUMBER_OF_QUESTIONS} questions.\n"\
         "Here is the session ID to this qiz:\n"\
         f"{session.id}")
    query.answer()
        
    return TEST_CREATION


# ---------------------------------------------------------------------------------------
# Register Conversation

@util.send_typing_action
def start_register(update:Update, context:CallbackContext):
    # TODO BOOK_MARK create steps for aquiring contact information
    user_id = update.message.from_user.id
    
    if models.User.objects.filter(user_id= user_id).exists():
        update.message.reply_text(
            "You have already registered. You can take a quiz by running the command /start_quiz",
            reply_markup= main_keyboard)
        return ConversationHandler.END
    
    contact_keyboard = [
        [KeyboardButton(text="Share Contact", request_contact= True), ('/cancel')],
     ]
    reply_markup = ReplyKeyboardMarkup(contact_keyboard, input_field_placeholder= "Press /cancel to cancel the process...")
    update.message.reply_text("Please share your contact information: ", reply_markup= reply_markup)
    return REG_CONTACT
        
@util.send_typing_action
def register_contact(update:Update, context:CallbackContext):
    contact = update.message.contact
    chat_id = update.message.chat_id
    # TODO make phone number reg ex or create a form
    user, create= models.User.objects.get_or_create(user_id = contact.user_id, chat_id= chat_id, username= contact.user_id)
    if create:
        user.first_name = contact.first_name
        user.last_name = contact.last_name
        user.phone_number = contact.phone_number
        user.set_unusable_password()
        user.save()
    else:
        update.message.reply_text("You have already registered!", reply_markup= ReplyKeyboardRemove())
        return ConversationHandler.END
    update.message.reply_text("Please share your education.", reply_markup= ReplyKeyboardRemove())
    return REG_EDUCATION


@util.send_typing_action
def register_education(update:Update, context:CallbackContext):
    # FIXME create a way to filter and authorize the education field
    message = update.message.text
    if message:
        chat_id = update.message.chat_id
        user = models.User.objects.get(chat_id= chat_id)
        user.education = message
        user.save()
        update.message.reply_text("Thank you for sharing your information! You can now start the test by running the command /start_quiz")
    # TODO handle reply messages that are not text or are not correctly formatted
    return ConversationHandler.END


# ---------------------------------------------------------------------------------------
# Quiz Conversation

@util.send_typing_action
def start_quiz(update:Update, context:CallbackContext):
    # TODO if the user is not registered, don't let him start the quiz
    user_id = update.message.from_user.id
    try:
        models.User.objects.get(user_id= user_id)
    except models.User.DoesNotExist:
        update.message.reply_text("You have not registered. Please register first by running the command /register")
        return ConversationHandler.END
    keyboard = [[InlineKeyboardButton("Start", callback_data= "subject_select")],
                [InlineKeyboardButton("Cancel", callback_data= "cancell")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Press to start the quiz: ", reply_markup=reply_markup)

    return SUBJECT_SELECT
    pass


@util.send_typing_action
def quiz(update:Update, context:CallbackContext):
    query = update.callback_query
    session_questions_ids = []
    data = query.data
    # print(data)
    
    if data == 'cancel':
        return cancel(update, context)
    
    # if we are here from the question select status
    elif re.match("^SESSIONID-\d+", data):
        # if the incoming query matches the session id we have in the last cllback, get all the sessions questions
        session_id = data.split('-')[1]
        session = models.Session.objects.get(id= session_id)
        session_questions_ids = util.get_session_question_ids(session)
        # get all the session_questions taht were selected in the session
        keyboard = [
            # format of the data sent by this button is: {session_question_id}-{index} - we send questions this way
            [InlineKeyboardButton("Go to Question 1", callback_data= f'{session_questions_ids[0]}-{0}')],
            [InlineKeyboardButton("Cancel", callback_data= "cancel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.edit_text("Select to go to the first question:", reply_markup= reply_markup)
        query.answer()

    # if we have a question 
    elif re.match("\d+-\d+", data):    
        # get session and session_question ids
        session_question_id, index = [int(item) for item in data.split("-")]
        session_question = models.SessionQuestion.objects.get(id= session_question_id)
        session_questions_ids = util.get_session_question_ids(session_question.session)
        question = session_question.question
        # the index for the question int the session_questions_ids list
        next_prev_buttons = []
        print(f"index: {index}")
        # we shouldn't have next button in the last question and previous button in the first question
        if index < len(session_questions_ids)-1:
            next_question_id = session_questions_ids[index+1]
            next_prev_buttons.append(InlineKeyboardButton("Next Test", callback_data= f"{next_question_id}-{index+1}"))
            
        if index >= 1:
            previous_question_id = session_questions_ids[index-1]
            next_prev_buttons.append(InlineKeyboardButton("Prevoius Test", callback_data= f"{previous_question_id}-{index-1}"))
            
        keyboard = [
            [
                InlineKeyboardButton(f"1- {question.op1}", callback_data= f'SESSION-{session_question.id}:OPTION-{1}'),
                InlineKeyboardButton(f"2- {question.op2}", callback_data= f'SESSION-{session_question.id}:OPTION-{2}')
            ],
            [
                InlineKeyboardButton(f"3- {question.op3}", callback_data= f'SESSION-{session_question.id}:OPTION-{3}'),
                InlineKeyboardButton(f"4- {question.op4}", callback_data= f'SESSION-{session_question.id}:OPTION-{4}')
            ],
            next_prev_buttons, # place holder for next and previous buttons
            [
                InlineKeyboardButton("Cancel", callback_data= "cancel")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.edit_text(f"Question No.{index+1}: {question.text}", reply_markup= reply_markup)
        query.answer()
    
    return QUIZ


# ---------------------------------------------------------------------------------------
# Main 

def main():
    from src.config.settings import TOKEN
    updater = Updater(token= TOKEN, use_context= True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level= logging.INFO)

    create_test_conversation = ConversationHandler(
        entry_points= [CommandHandler('create_quiz', create_quiz)],
        states= {
            SUBJECT_SELECT: [CallbackQueryHandler(subject_select, pattern= 'subject_select')],
            QUESTION_SELECT: [CallbackQueryHandler(question_select, pattern= "^SUBID-\d+")],
            TEST_CREATION: []
            },
        fallbacks= [
            CommandHandler('cancel', cancel),
            CallbackQueryHandler(cancel, pattern= 'cancel')
            ]
    )

    quiz_conversation = ConversationHandler(
        # this function sends this callback_data -> "subj_sel"
        entry_points= [CommandHandler('start_quiz', start_quiz)],
        states={
            QUIZ: [CallbackQueryHandler(quiz)],
            },
        fallbacks= [
            CommandHandler('cancel', cancel),
            CallbackQueryHandler(cancel, pattern= 'cancel')
            ]
    )
    
    register_conversation = ConversationHandler(
        entry_points= [CommandHandler('register', start_register)],
        states={
            REG_CONTACT: [
                MessageHandler(Filters.contact, register_contact),
                ],
            REG_EDUCATION: [
                MessageHandler(Filters.text, register_education)
            ]
            },
        fallbacks= [CommandHandler('cancel', cancel)],
    )
    
    handlers = [
        CommandHandler('start', start),
        # quiz_conversation, 
        register_conversation,
        create_test_conversation
    ]
    
    for handler in handlers: 
        dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()