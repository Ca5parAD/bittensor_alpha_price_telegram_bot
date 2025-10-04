import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler

from utils import *
from messages import *
from simple_commands import show_commands
from taostats_calls import valid_netuids_check
from notification_handling import set_notifications
from debugging import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - settings command")
    # Obtain and store user settings
    notification_status = "🔔 On" if context.user_data.get('send_notifications_flag', False) else "🔕 Off"
    subnets = context.user_data.get('notification_netuids', [])
    frequency = context.user_data.get('notification_frequency', 'Not set')
    if not frequency % 1: # Store frequency as int if possible
        frequency = int(frequency)
    
    # Format and print user settings
    await update.message.reply_text(
        f"<b>Current Settings</b> ⚙️\n"
        f"Receive notifications: {notification_status}\n"
        f"Selected subnets: {subnets or 'None'} 📌\n"
        f"Notification frequency: {frequency} ⏰\n\n",
        parse_mode="HTML"
    )
    await update.message.reply_text(SETTINGS_COMMANDS_MESSAGE, parse_mode="HTML")
    return SELECT_SETTING

# Toggles send notification flag
async def enable_disable(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - enable/disable")
    context.user_data['send_notifications_flag'] = not context.user_data['send_notifications_flag']

    await set_notifications(update, context)
    return await settings_command(update, context)

# Prompt user to input subnets
async def select_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - select subnets")
    await update.message.reply_text(SELECT_SUBNETS_MESSAGE, parse_mode="HTML")
    return ENTER_SUBNETS

async def store_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - store subnets")
    text = update.message.text.strip() # Store user response
    logger.debug(f"user_id:{update.effective_user.id} - user input: {text}")

    try: # Check validity of user response
        valid_netuids, invalid_netuids = valid_netuids_check(text)

    except ValueError as e: # Does this need to specify ValueError? ********** # Show user message if invalid text
        logger.debug(f"user_id:{update.effective_user.id} - invalid input: {text} - {str(e)}")
        await update.message.reply_text(INVALID_PROCESS_NETUID, parse_mode="HTML")
        return ENTER_ALPHA_PRICE  # Stay in state for retry

    else:
        context.user_data['notification_netuids'] = valid_netuids
        logger.debug(f"user_id:{update.effective_user.id} - storing netuids: {valid_netuids}")
        # Show user message for invalid subnets
        if invalid_netuids:
            invalid_netuids_message = "⚠️ Invalid subnet(s):\n"
            for netuid in invalid_netuids:
                invalid_netuids_message += f"{netuid}\n"
                await update.message.reply_text(invalid_netuids_message)

        return await settings_command(update, context)


# Prompt user to select notification frequency
async def select_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - select notification frequency")
    await update.message.reply_text(SELECT_NOTIFICATION_FREQUENCY_MESSAGE, parse_mode="HTML")
    return SELECT_NOTIF_FREQ

async def store_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - store Notification Frequency")
    text = update.message.text # Store user response

    # Set hour user frequency to mapping of input
    freq_map = {'/1hr': 1, '/4hrs': 4, '/12hrs': 12, '/1D': 24}
    context.user_data['notification_frequency'] = freq_map[text]
    await set_notifications(update, context)
    return await settings_command(update, context)


# Prompt user to input custom notification frequency
async def custom_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - custom notification frequency")
    await update.message.reply_text(CUSTOM_NOTIFICATION_FREQUENCY_MESSAGE, parse_mode="HTML")
    return CUSTOM_NOTIF_FREQ

async def store_custom_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - store custom notification frequency")
    text = update.message.text.strip() # Store user response

    try:
        interval = float(text)

    except ValueError as e:
        logger.error(f"user_id:{update.effective_user.id} - invalid input: {text} - {str(e)}")
        await update.message.reply_text("Invalid input. Please try again")
        return ENTER_SUBNETS  # Stay in state for retry

    else:
        context.user_data['notification_frequency'] = interval
        logger.info(f"user_id:{update.effective_user.id} - set notification frequency to {interval}")
        await set_notifications(update, context)
        return await settings_command(update, context)

# Functions to go back in conversation
async def back_select_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - back")
    return await show_commands(update, context)

async def back_select_setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - back")
    return await settings_command(update, context)

async def back_select_notif_freq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.effective_user.id} - back")
    return await select_notification_frequency(update, context)


# Valid specific commands per state
select_setting_commands = [
    CommandHandler("enable_disable", enable_disable),
    CommandHandler("select_sns", select_subnets),
    CommandHandler("notification_frequency", select_notification_frequency),
    CommandHandler("back", back_select_command),
    CommandHandler("test", test_notifications),
    CommandHandler("user_data", test_user_data)
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
    CommandHandler("custom", custom_notification_frequency),
    CommandHandler("back", back_select_setting)
]

custom_notification_frequency_commands = [
    CommandHandler("back", back_select_setting),
    MessageHandler(filters.TEXT & ~filters.COMMAND, store_custom_notification_frequency)
]