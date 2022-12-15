import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import os
import re
import requests
import datetime
import json

version_id = "0.0.1"

user_request = {}

# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="/canpickup OR /needride")

def version(update, context):
    print("Version is:" + version_id)
    update.message.reply_text("Version is:" + version_id)
    return


# Define the function to handle the /pickup command
def pickup_command(update, context):
    # Get the chat id
    chat_id = update.message.chat_id
    user_request["type"] = "can pickup someone"
    # Create the keyboard with the 2 options
    keyboard = [['to-train', 'from-train']]
    # Send a message to the user with the keyboard
    context.bot.send_message(chat_id=chat_id, text='Select the direction:', reply_markup=telegram.ReplyKeyboardMarkup(keyboard))

# Define the function to handle the /pickup command
def ride_command(update, context):
    # Get the chat id
    chat_id = update.message.chat_id
    user_request["type"] = "want to ride with someone"
    # Create the keyboard with the 2 options
    keyboard = [['to-train', 'from-train']]
    # Send a message to the user with the keyboard
    context.bot.send_message(chat_id=chat_id, text='Select the direction:', reply_markup=telegram.ReplyKeyboardMarkup(keyboard))

# Define the function to handle the to-train and from-train options
def pick_train(update, context):
    # Get the chat id
    chat_id = update.message.chat_id
    # Get the selected option
    option = update.message.text
    user_request["direction"] = option

    # Create the keyboard with the 2 options
    keyboard = [['today', 'tomorrow']]
    # Send a message to the user with the keyboard
    context.bot.send_message(chat_id=chat_id, text='Select day:', reply_markup=telegram.ReplyKeyboardMarkup(keyboard))

# Define the function to handle the today and tomorrow options
def pick_date(update, context):
    # Get the chat id
    chat_id = update.message.chat_id
    # Get the selected option
    option = update.message.text
    user_request["day"] = option

    # Create the keyboard with the time options
    keyboard = [['06:06 AM', '06:39 AM'], ['07:06 AM', '07:39 AM'], ['08:06 AM', '08:39 AM']]
    # Send a message to the user with the keyboard
    context.bot.send_message(chat_id=chat_id, text='Select train time:', reply_markup=telegram.ReplyKeyboardMarkup(keyboard))

def save_query(update, context):
    # Get the chat id
    chat_id = update.message.chat_id
    # Get the selected option
    option = update.message.text
    user_request["time"] = option

    # Send a message to the user with the summary
    text = "You've indicated that you " + user_request["type"] + " " + user_request["direction"] + " " + \
        user_request["day"] + " at " + user_request["time"]
    context.bot.send_message(chat_id=chat_id, text=text)





telegram_bot_token = os.environ['TGRM_TKN']
if telegram_bot_token != 'TEST':
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("version", version))

    # run the start function when the user invokes the /start command 
    dispatcher.add_handler(CommandHandler("start", start))

    # Add the command handler for the /pickup command
    dispatcher.add_handler(CommandHandler('canpickup', pickup_command))

    # Add the message handler for the to-train and from-train options
    dispatcher.add_handler(MessageHandler(Filters.regex('^(to-train|from-train)$'), pick_train))

    # Add the message handler for the today and tomorrow options
    dispatcher.add_handler(MessageHandler(Filters.regex('^(today|tomorrow)$'), pick_date))

    dispatcher.add_handler(MessageHandler(Filters.regex('^\d\d:\d\d [AP]M$'), save_query))


    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                        port=int(os.environ.get('PORT', 5243)),
                        url_path=telegram_bot_token,
                        webhook_url= 'https://gilon-train-lift.up.railway.app/' + telegram_bot_token
                        )