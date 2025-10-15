import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from utils import *
from user_settings import setup_settings
from messages import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bolts on setup and welcome message to show_commands"""
    logger.info(f"user_id:{update.effective_user.id} - start command")
    setup_settings(update.effective_user.id, context.user_data)
    await update.message.reply_text(START_MESSAGE, parse_mode="HTML")
    return await show_commands(update, context)

async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows user top level directions"""
    logger.info(f"user_id:{update.effective_user.id} - show commands")
    await update.message.reply_text(SHOW_COMMANDS_MESSAGE, parse_mode="HTML")
    return SELECT_COMMAND

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows user full program commands"""
    logger.info(f"user_id:{update.effective_user.id} - help command")
    await update.message.reply_text(HELP_MESSAGE, parse_mode="HTML")
    return HELP

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"user_id:{update.effective_user.id} - unknown command")
    await update.message.reply_text(UNKNOWN_COMMAND, parse_mode="HTML")

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"user_id:{update.effective_user.id} - unknown message")
    await update.message.reply_text(UNKNOWN_MESSAGE, parse_mode="HTML")

async def outside_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unrecognised message outside of conversation flow"""
    logger.info(f"user_id:{update.effective_user.id} - outside conversation")
    await update.message.reply_text(OUTSIDE_CONVERSATION_MESSAGE, parse_mode="HTML")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.exception(f"user_id:{update.effective_user.id} - update caused error: {context.error}")
    await update.message.reply_text(ERROR_MESSAGE, parse_mode="HTML")


outside_conversation_handler = MessageHandler(filters.TEXT, outside_conversation)