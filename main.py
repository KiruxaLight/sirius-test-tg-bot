#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.text == "aboba":
        update.message.reply_text("abobus")
    else:
        update.message.reply_text(update.message.text)


names = ['Гарри', 'Рона', 'Гермиону', 'Драко', 'Альбуса', 'Хагрида', 'Тома']


def harry_potter(query, update, context: CallbackContext) -> None:
    my_random = random.Random(update.effective_user)
    query.edit_message_text("Ты похож на " + str(my_random.randint(0, 100)) + "% на " + str(names[my_random.randint(0, len(names) - 1)]) + " из Гарри Поттера")


def your_iq(query, update, context: CallbackContext) -> None:
    my_random = random.Random(update.effective_user)
    query.edit_message_text("Твой IQ - " + str(my_random.randint(0, 300)))

def amogus(query, update, context: CallbackContext) -> None:
    my_random = random.Random(update.effective_user)
    a = my_random.randint(1, 2)
    if a == 1:
        query.edit_message_text("Амогус")
    else:
        query.edit_message_text("Не амогус")


#abobus amogus sus

def who(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Кто ты из Гарри Поттера", callback_data = '1')],
        [InlineKeyboardButton("Сколько у тебя IQ", callback_data = '2')],
        [InlineKeyboardButton("Амогус?", callback_data='3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Узнай:", reply_markup = reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == '1':
        harry_potter(query, update, context)
    elif query.data == '2':
        your_iq(query, update, context)
    elif query.data == '3':
        amogus(query, update, context)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5047104585:AAHBvgcT8vdUShQmRCl2nmqxljwURqsoFQQ")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("who", who))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()