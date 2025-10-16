import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler

from utils import *
from messages import *
from simple_commands import show_commands
from taostats_calls import valid_netuids_check
from notification_handling import set_notifications
from data_persistance import update_database_user_settings
from debugging import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prints current user settings and prompts to select which setting to change"""
    logger.info(f"user_id:{update.effective_user.id} - settings command")
    # Obtain and store user settings
    notification_status = "🔔 On" if context.user_data.get('send_notifications', False) else "🔕 Off"
    subnets = context.user_data.get('notification_subnets', [])
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

async def enable_disable(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Toggles on/off notificaitions"""
    user_id = update.effective_user.id
    logger.info(f"user_id:{user_id} - enable/disable")
    context.user_data['send_notifications'] = not context.user_data['send_notifications']

    try: # Update database for user settings
        update_database_user_settings(user_id, context.user_data)
    except: # TODO fix logging message
        logger.info("fail 1")

    try:
        set_notifications(user_id, context.user_data)
    except Exception:
        await update.message.reply_text("Failed to set notifications, please try again later")
    return await settings_command(update, context)


async def select_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to input subnets"""
    logger.info(f"user_id:{update.effective_user.id} - select subnets")
    await update.message.reply_text(SELECT_SUBNETS_MESSAGE, parse_mode="HTML")
    return ENTER_SUBNETS

async def store_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes text and stores netuids"""
    user_id = update.effective_user.id
    logger.info(f"user_id:{user_id} - store subnets")
    text = update.message.text.strip() # Store user response
    logger.debug(f"user_id:{user_id} - user input: {text}")

    try: # Check validity of netuids seleted
        valid_subnets, invalid_netuids = valid_netuids_check(text)

    # TODO Does this need to specify ValueError?
    except ValueError as e: # Show user message if invalid text
        logger.debug(f"user_id:{user_id} - invalid input: {text} - {str(e)}")
        await update.message.reply_text(INVALID_PROCESS_NETUIDS, parse_mode="HTML")
        return ENTER_ALPHA_PRICE # Stay in state for retry

    else:
        context.user_data['notification_subnets'] = valid_subnets
        logger.debug(f"user_id:{user_id} - storing subnets: {valid_subnets}")

        try:
            update_database_user_settings(user_id, context.user_data)
        except:
            logger.info("fail 2") # TODO fix logging message

        if invalid_netuids: # Show user message for invalid subnets
            invalid_netuids_message = "⚠️ Invalid subnet(s):\n"
            for netuid in invalid_netuids:
                invalid_netuids_message += f"{netuid}\n"
                await update.message.reply_text(invalid_netuids_message)

        return await settings_command(update, context)


async def select_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to select notification frequency"""
    logger.info(f"user_id:{update.effective_user.id} - select notification frequency")
    await update.message.reply_text(SELECT_NOTIFICATION_FREQUENCY_MESSAGE, parse_mode="HTML")
    return SELECT_NOTIF_FREQ

async def store_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Set notification frequency selected by user"""
    user_id = update.effective_user.id
    logger.info(f"user_id:{user_id} - store Notification Frequency")
    text = update.message.text # Store user response

    # Command and hour int mapping of input
    freq_map = {'/1hr': 1, '/4hrs': 4, '/12hrs': 12, '/1D': 24}
    context.user_data['notification_frequency'] = freq_map[text]

    try:
        update_database_user_settings(user_id, context.user_data)
    except:
        logger.info("fail 3") # TODO fix logging message
    
    try:
        set_notifications(user_id, context.user_data)
    except Exception as e:
        logger.error(
            f"user_id:{user_id} - Failed to create notification job: {e}",
            exc_info=True
        )
        await update.message.reply_text("Failed to set notifications, please try again later")
    return await settings_command(update, context)

async def custom_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to input custom notification frequency"""
    logger.info(f"user_id:{update.effective_user.id} - custom notification frequency")
    await update.message.reply_text(CUSTOM_NOTIFICATION_FREQUENCY_MESSAGE, parse_mode="HTML")
    return CUSTOM_NOTIF_FREQ

async def store_custom_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process and set custom notification frequency"""
    user_id = update.effective_user.id
    logger.info(f"user_id:{user_id} - store custom notification frequency")
    text = update.message.text.strip() # Store user response

    try:
        interval = float(text)

    except ValueError as e:
        logger.error(f"user_id:{user_id} - invalid input: {text} - {str(e)}")
        await update.message.reply_text("Invalid input. Please try again")
        return ENTER_SUBNETS  # Stay in state for retry

    else:
        context.user_data['notification_frequency'] = interval
        logger.info(f"user_id:{user_id} - set notification frequency to {interval}")

        try:
            update_database_user_settings(user_id, context.user_data)
        except:
            logger.info("fail 4") # TODO fix logging message

        try:
            set_notifications(user_id, context.user_data)
        except Exception as e:
            logger.error(
                f"user_id:{user_id} - Failed to create notification job: {e}",
                exc_info=True
            )
            await update.message.reply_text("Failed to set notifications, please try again later")
        return await settings_command(update, context)

# Functions to go back in conversation
async def back_select_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Back to main menu"""
    logger.info(f"user_id:{update.effective_user.id} - back")
    return await show_commands(update, context)

async def back_select_setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Back to settings menu"""
    logger.info(f"user_id:{update.effective_user.id} - back")
    return await settings_command(update, context)

async def back_select_notif_freq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Back to select notification frequency menu"""
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