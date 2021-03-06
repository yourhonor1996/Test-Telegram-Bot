
# TODO optimize regex handling in the conversations and cerate data dictionaries for them
# TODO create a file for storing constants like callback actions or keyboard buttons
# TODO since the data limit for a callback data is 64-bit data, we should figure out nother way for sending data in the callback queries 

import telegram
from telegram import ext
from telegram.constants import PARSEMODE_HTML
# first we have to config django settings so we can use the ORM Module.
from src.utility.util import config_django
config_django()

from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, InlineQueryResultArticle,
    InputTextMessageContent, ParseMode)
from telegram.ext import Updater
from telegram.ext import (
    CommandHandler,CallbackQueryHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext, InlineQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

import logging
from src.utility.util import logger
from src import models
from src.config import settings
from src.utility import util
from django.utils import timezone
import re
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.error import BadRequest
from telegram.utils.helpers import create_deep_linked_url

# create_quiz states
SUBJECT_SELECT, QUESTION_SELECT, TEST_CREATION = CREATE_TEST_STATES = range(3)
# quiz states
QUIZ, RESULTS = MAIN_PHASES = range(len(CREATE_TEST_STATES), len(CREATE_TEST_STATES) + 2)
# registry states
REG_CONTACT, REG_EDUCATION= REG_PHASES = range(len(MAIN_PHASES), len(MAIN_PHASES)+2)

main_keyboard = ReplyKeyboardMarkup(
        [['/help', '/register'],
        ['/create_quiz', '/start_quiz']],
        one_time_keyboard= True,
        input_field_placeholder= 'Enter the command here...')


# ---------------------------------------------------------------------------------------
# Global functions

def help(update:Update, context:CallbackContext):
    message = \
    "Hello this is a quiz telegram bot. Here are the commands:\n" \
    "If you haven't registered you can register via /register" \
    "You can create a test and share it with your firends via /create_quiz\n" \
    "You can start a quiz via /start_quiz"
    
    # update.message.reply_text(str(arguments))
    update.message.reply_text(message, reply_markup= main_keyboard)
    # if len(arguments) == 1:
    #     start_quiz(update, context)
    #     # return QUIZ

@util.send_typing_action
def cancel(update:Update, context:CallbackContext):
    this_udpate = util.get_update(update, context)
    this_udpate.message.reply_text("Canceled the process.", reply_markup= ReplyKeyboardRemove())
    this_udpate.answer()
    return ConversationHandler.END


def authorize_user(update:Update, context:CallbackContext):
    user_id = update.message.from_user.id
    if models.User.objects.filter(user_id= user_id).exists():
        return True
    else:
        update.message.reply_text(
            "You have not registered. Please register first by running the command /register",
            reply_markup= main_keyboard)
        return False
    

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    # if the inline query has the proper session id then prompt to take the test:
    try:
        session = models.Session.objects.get(id= int(query))
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"Session ID: {session.id}\nQuiz Title: {session.quiz.title}",
                input_message_content= InputTextMessageContent(
                    escape_markdown(f"/start {query}"),
                    parse_mode= ParseMode.MARKDOWN_V2)
            )]
    except models.Session.DoesNotExist:
        results = [
            InlineQueryResultArticle(
            id=str(uuid4()),
            title="No quiz found...",
            input_message_content=  InputTextMessageContent("No quiz found...")
        )]

    update.inline_query.answer(results)

# ---------------------------------------------------------------------------------------
# Create Test Converstation

def create_quiz(update:Update, context:CallbackContext):
    if not authorize_user(update, context):
        return ConversationHandler.END 
    
    keyboard = [[InlineKeyboardButton("Start", callback_data= "subject_select")],
                [InlineKeyboardButton("Cancel", callback_data= "cancellqef")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Press to create the quiz: ", reply_markup=reply_markup)

    return SUBJECT_SELECT


@util.send_typing_action
def subject_select(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    # TODO make the subjects appear in two columns
    subjects = models.Subject.objects.all().values_list('id', 'name')
    keyboard = [[InlineKeyboardButton("Cancel", callback_data= "cancel")]]
    for id, name in subjects:
        keyboard.append([InlineKeyboardButton(f'{name}', callback_data= f'SUBID-{id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(text= 'Please choose the subject:', reply_markup=reply_markup)
    return QUESTION_SELECT

# TODO create a conversation to ask the user how many users he wants for this quiz

util.send_typing_action
def question_select(update:Update, context:CallbackContext):
    # get initial data
    now = timezone.now()
    query = update.callback_query
    query.answer()
    user = models.User.objects.get(user_id= util.get_user(update, context).id)
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
    # TODO create a conversation to ask the user how many users he wants for this quiz
    session.users_to_start = settings.NUMBER_OF_USERS_FOR_SESSION
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


    # create a deep link to this session with the session ID
    bot = context.bot
    url = create_deep_linked_url(bot.username, f"{session.id}" , group=False)
    print(url)
    subject = models.Subject.objects.get(id= subject_id)
    text = f"You have chosen {subject.name}. Your quiz has {settings.NUMBER_OF_QUESTIONS} questions.\n"\
        f"Here is the session ID to this qiz: {session.id}\n"\
        f"You can share this message with your firend so you can start this test together."
    keyboard = [
        [InlineKeyboardButton(f"Quiz: {quiz.title}-{session.id}", url= url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(
        text= text,
        reply_markup= reply_markup
       )
        
    return TEST_CREATION


# ---------------------------------------------------------------------------------------
# Register Conversation

def start_register(update:Update, context:CallbackContext):
    # TODO BOOK_MARK create steps for aquiring contact information
    user_id = update.message.from_user.id
    
    if authorize_user(update, context):
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
def create_question_keyboard(session_question, index:int):
    session_questions_ids = util.get_session_question_ids(session_question.session)
    next_prev_buttons = []
    length = len(session_questions_ids)
    # index = int(index)
    print(f"index: {index}")
    # we shouldn't have next button in the last question and previous button in the first question
    if index >= 1:
        previous_question_id = session_questions_ids[index-1]
        next_prev_buttons.append(InlineKeyboardButton("Prevoius Test", callback_data= f"{previous_question_id}-{index-1}"))

    if index < length-1:
        next_question_id = session_questions_ids[index+1]
        next_prev_buttons.append(InlineKeyboardButton("Next Test", callback_data= f"{next_question_id}-{index+1}"))

        
    keyboard = [
        [
            InlineKeyboardButton(f"1- {session_question.question.op1}", callback_data= f'{session_question.id}-{index}-{1}'),
            InlineKeyboardButton(f"2- {session_question.question.op2}", callback_data= f'{session_question.id}-{index}-{2}')
        ],
        [
            InlineKeyboardButton(f"3- {session_question.question.op3}", callback_data= f'{session_question.id}-{index}-{3}'),
            InlineKeyboardButton(f"4- {session_question.question.op4}", callback_data= f'{session_question.id}-{index}-{4}')
        ],
        next_prev_buttons, # place holder for next and previous buttons
        [
            InlineKeyboardButton("Cancel", callback_data= "cancel")
        ]
    ]

    # if we at the last question, create the option to submit the answer.
    if index == length-1:
        keyboard.append(
            [InlineKeyboardButton("Submit Test", callback_data= f"submit_quiz-{session_question.id}")])
    
    return keyboard


def start_quiz(update:Update, context:CallbackContext):
    # TODO if the user is not registered, don't let him start the quiz
    if not authorize_user(update, context):
        help(update, context)
        return ConversationHandler.END
    
    arguments = context.args
    if len(arguments) == 0:
        help(update, context)
        return ConversationHandler.END    
    
    elif len(arguments) == 1:
        try:
            session = models.Session.objects.get(id= arguments[0])
        except models.Session.DoesNotExist:
            update.message.reply_text(f"There is no quiz with id {arguments[0]}", reply_markup= main_keyboard)
            return ConversationHandler.END    

    keyboard = [[InlineKeyboardButton(f"Start quiz with id {session.id}", callback_data= f"SESSIONID-{session.id}")],
                [InlineKeyboardButton("Cancel", callback_data= "cancel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Press to start the quiz: ", reply_markup=reply_markup)

    return QUIZ


@util.send_typing_action
def quiz(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    session_questions_ids = []
    data = query.data
    user = models.User.objects.get(user_id= util.get_user(update, context).id)
    
    # if the data were to cancel the test
    if data == 'cancel':
        return cancel(update, context)
    
    # if we want to submit the answer, go to the next state
    elif re.match('submit_quiz-\d+', data):
        # TODO what could go wrong in this get method?
        session_question_id = int(data.split('-')[1])
        # this is the last session_question sent from the submit button
        last_session_question = models.SessionQuestion.objects.get(id= session_question_id)
        session = last_session_question.session
        keyboard_ = [
            [InlineKeyboardButton("Submit Test Answer", callback_data= f'{session.id}')]
        ]
        text = "Are you sure you want to submit the test results?"
        query.message.edit_text(text= text, reply_markup= InlineKeyboardMarkup(keyboard_))
        print(f"data in quiz:{data}")
        return RESULTS
    
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

    # if we have a request for loading for a question or we have an answer
    elif re.match("\d+-\d+", data) or re.match("^\d+-\d+-\d+", data):    
        data_split = [int(item) for item in query.data.split("-")]
        
        if len(data_split) == 2:
            session_question_id, index = data_split

        if len(data_split) == 3:
            session_question_id, index, submitted_answer = data_split
            
        # find the session_question so we can build our data based on it
        session_question = models.SessionQuestion.objects.get(id= session_question_id)
        question = session_question.question

        keyboard = create_question_keyboard(session_question, index)
        # if we have a question
        if re.match("\d+-\d+", data):
            try:
                session_answer = models.SessionAnswer.objects.get(
                    session= session_question.session,
                    question= session_question.question,
                    user= user)
                data_base_answer = session_answer.submitted_test_answer
            except models.SessionAnswer.DoesNotExist:
                data_base_answer = None

        # if we have a request for an answer
        if re.match("^\d+-\d+-\d+", data):
            print(data)
            try:
                session_answer = models.SessionAnswer.objects.get( 
                    session= session_question.session,
                    question= session_question.question,
                    user= user)
            except models.SessionAnswer.DoesNotExist:
                session_answer = models.SessionAnswer.objects.create( 
                    session= session_question.session,
                    question= session_question.question,
                    user= user,
                    submitted_test_answer= submitted_answer)
            finally:
                session_answer.submitted_test_answer = submitted_answer
                session_answer.date_answered = timezone.now()
                session_answer.save()
            
            data_base_answer = session_answer.submitted_test_answer
                
        emoji = settings.CHECK_EMOJI
        if data_base_answer == 1:
            keyboard[0][0].text += emoji
        elif data_base_answer == 2:
            keyboard[0][1].text += emoji
        elif data_base_answer == 3:
            keyboard[1][0].text += emoji
        elif data_base_answer == 4:
            keyboard[1][1].text += emoji
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.edit_text(f"Question No.{index+1}: {question.text}", reply_markup= reply_markup)


def results(update:Update, context:CallbackContext):
    # show the results to the user
    query = update.callback_query
    print(f"data in results:{query.data}")
    user = models.User.objects.get(user_id= util.get_user(update, context).id)
    session_id = int(query.data)
    query.answer()
    session = models.Session.objects.get(id= session_id)

    # get all the answers that were submitted by this user
    results_report = session.session_report
    for item in results_report:
        # query.message.reply_text(text= str(item))
        text = util.create_quiz_report(item)
        query.message.reply_text(text= text)
    # query.message.reply_text(text= str(results_report))
    return ConversationHandler.END
        


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
        entry_points= [
            # CommandHandler('start', start),
            CommandHandler('start', start_quiz)
            ],
        states={
            QUIZ: [
                CallbackQueryHandler(quiz),
                ],
            RESULTS: [
                CallbackQueryHandler(results)
            ]
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
        CommandHandler('help', help),
        quiz_conversation, 
        register_conversation,
        create_test_conversation,
        InlineQueryHandler(inlinequery)
    ]
    
    for handler in handlers: 
        dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()