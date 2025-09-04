import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler

from utils import SELECT_SETTING, ENTER_SUBNETS, SELECT_NOTIF_FREQ, SELECT_COMMAND
from messages import SETTINGS_COMMANDS_MESSAGE, SELECT_SUBNETS_MESSAGE, SELECT_NOTIFICATION_FREQUENCY_MESSAGE
from notification_handling import set_notifications
from simple_commands import top_level_directions
from bittensor_calls import valid_subnets_check

logger = logging.getLogger(__name__)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("settings command")
    await update.message.reply_text(
        f"Your current settings:\n\
        Receive notifications: {context.user_data['send_notifications_flag']}\n\
        Selected subnets: {context.user_data['notification_subnets']}\n\
        Notification frequency: {context.user_data['notification_frequency']}"
    )
    await update.message.reply_text(SETTINGS_COMMANDS_MESSAGE)

    return SELECT_SETTING

async def enable_disable(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("enable/disable")
    context.user_data['send_notifications_flag'] = not context.user_data['send_notifications_flag']

    # Check this
    set_notifications(update, context)

    return await settings_command(update, context)


async def select_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("select subnets")
    await update.message.reply_text(SELECT_SUBNETS_MESSAGE)
    return ENTER_SUBNETS

async def store_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("store subnets")
    text = update.message.text.strip()

    try:
        valid_subnets, invalid_subnets = valid_subnets_check(text)
        context.user_data['notification_subnets'] = valid_subnets
        logger.info(f"Stored subnets: {valid_subnets}")
        await update.message.reply_text(f"Cool! Subnets stored: {valid_subnets}")
        return await settings_command(update, context)
 
    except ValueError as e:
        logger.error(f"Invalid input: {text} - {str(e)}")
        await update.message.reply_text("Invalid input. Please enter subnet IDs (0-128) separated by commas (e.g. 5,7,19,64)")
        return ENTER_SUBNETS  # Stay in this state for retry


async def select_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("select notification frequency")
    await update.message.reply_text(SELECT_NOTIFICATION_FREQUENCY_MESSAGE)
    return SELECT_NOTIF_FREQ


async def store_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Store Notification Frequency")
    text = update.message.text
    freq_map = {'/1hr': 1, '/4hrs': 4, '/12hrs': 12, '/1D': 24}
    
    if text in freq_map:
        context.user_data['notification_frequency'] = freq_map[text]
        logger.info(f"Set notification frequency to {freq_map[text]}")
        await update.message.reply_text(f"You will recieve a notification every {freq_map[text]}hrs")
        set_notifications(update, context)
        return await settings_command(update, context)
    else:
        logger.error(f"Invalid frequency: {text}")
        await update.message.reply_text("That was not an option. Choose: /1hr, /4hrs, /12hrs, /1D or /back")
        return SELECT_NOTIF_FREQ




async def back_select_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("back")
    return await top_level_directions(update, context)

async def back_select_setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("back")
    return await settings_command(update, context)







select_setting_commands = [
    CommandHandler("enable_disable", enable_disable),
    CommandHandler("select_sns", select_subnets),
    CommandHandler("notification_frequency", select_notification_frequency),
    CommandHandler("back", back_select_command)
]


enter_subnets_commands = [
    CommandHandler("back", back_select_setting),
    MessageHandler(filters.TEXT & ~filters.COMMAND, store_subnets)
]



select_notification_frequency_commands = [
    CommandHandler("1hr", store_notification_frequency),
    CommandHandler("4hrs", store_notification_frequency),
    CommandHandler("12hrs", store_notification_frequency),
    CommandHandler("1D", store_notification_frequency),
    CommandHandler("back", back_select_setting)
]

