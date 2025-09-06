import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from messages import *
from utils import *


logger = logging.getLogger(__name__)


# Start command bolts on setup and welcome message to top level directions
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("start command")
    reset_settings(update, context)
    await update.message.reply_text(START_MESSAGE, parse_mode="HTML")
    return await show_commands(update, context)

async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("top level directions")
    await update.message.reply_text(TOP_LEVEL_DIRECTIONS_MESSAGE, parse_mode="HTML")
    return SELECT_COMMAND

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("help command")
    await update.message.reply_text(HELP_MESSAGE, parse_mode="HTML")
    return HELP

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Unknown command")
    await update.message.reply_text(UNKNOWN_COMMAND, parse_mode="HTML")

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Unknown message")
    await update.message.reply_text(UNKNOWN_MESSAGE, parse_mode="HTML")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.exception(f"Update caused error: {context.error}")
    # Message to user about error
    # Way to reset conversation flow to user?


universal_handlers = [
    CommandHandler('start', start_command),
    CommandHandler('show_commands', show_commands),
    CommandHandler('help', help_command),
    MessageHandler(filters.COMMAND, unknown_command),
    MessageHandler(filters.TEXT, unknown_message)
]

