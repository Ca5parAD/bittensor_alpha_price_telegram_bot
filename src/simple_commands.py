import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from messages import START_MESSAGE,TOP_LEVEL_DIRECTIONS_MESSAGE, HELP_MESSAGE, UNKOWN_COMMAND_MESSAGE, UNKOWN_MESSAGE_MESSAGE
from utils import SELECT_COMMAND, reset_settings


logger = logging.getLogger(__name__)



# Start command bolts on setup and welcome message to top level directions
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("start command")
    reset_settings(update, context)
    await update.message.reply_text(START_MESSAGE)
    return await top_level_directions(update, context)

async def top_level_directions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("top level directions")
    await update.message.reply_text(TOP_LEVEL_DIRECTIONS_MESSAGE)
    return SELECT_COMMAND


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("help command")
    await update.message.reply_text(HELP_MESSAGE)
help_handler = CommandHandler('help', help_command)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Unknown command")
    await update.message.reply_text(UNKOWN_COMMAND_MESSAGE)
unkown_command_handler = MessageHandler(filters.COMMAND, unknown_command)

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Unknown message")
    await update.message.reply_text(UNKOWN_MESSAGE_MESSAGE)
unkown_command_handler = MessageHandler(filters.TEXT, unknown_message)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.exception(f"Update caused error: {context.error}")
    # Message to user about error
    # Way to reset conversation flow to user?