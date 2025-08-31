from messages import SETTINGS_COMMANDS_MESSAGE, SELECT_SUBNETS_MESSAGE, SELECT_NOTIFICATION_FREQUENCY_MESSAGE
from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler

from notification_handling import set_notifications
import logging

logger = logging.getLogger(__name__)


# Conversation states
ENTER_SETTING_STATE, STORE_SUBNETS_STATE, STORE_NOTIFICATION_FREQUENCY_STATE = range(3)

async def show_current_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Your current settings:\n\
        Receive notifications: {context.user_data['send_notifications_flag']}\n\
        Selected subnets: {context.user_data['notification_subnets']}\n\
        Notification frequency: {context.user_data['notification_frequency']}"
    )
    await update.message.reply_text(SETTINGS_COMMANDS_MESSAGE) 

# Prints current settings and list of commands
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Notification Settings Conversation Started")
    await show_current_settings(update, context)
    return ENTER_SETTING_STATE

# Toggles on/off whether user recieves notifications
async def enable_disable(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("enable/disable")
    context.user_data['send_notifications_flag'] = not context.user_data['send_notifications_flag']
    set_notifications(update, context)
    await show_current_settings(update, context)
    return ENTER_SETTING_STATE

# Displays instructions of user input for subnets to be tracked
async def select_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Select Subnets")
    await update.message.reply_text(SELECT_SUBNETS_MESSAGE)
    return STORE_SUBNETS_STATE

# Stores selected subnets
async def store_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Select Subnets")

    # Check through this logic - especially splitting the strings into ints
    text = update.message.text.strip()
    try:
        sns = [int(s) for s in text.split(',') if 0 <= int(s) <= 128]
        if sns:
            context.user_data['notification_subnets'] = sns
            logger.debug(f"Selected subnets: {sns}")
            await update.message.reply_text(f"Tracking subnets: {sns}")
            set_notifications(update, context)
            show_current_settings(update, context)
            return ENTER_SETTING_STATE
        else:
            raise ValueError("Invalid subnet IDs")
    except ValueError:
        logger.error(f"Invalid subnet IDs: {text}")
        await update.message.reply_text("Invalid subnet IDs (0-128), try again or /back")
        return STORE_SUBNETS_STATE


async def select_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Select Notification Frequency")
    await update.message.reply_text(SELECT_NOTIFICATION_FREQUENCY_MESSAGE)
    return STORE_NOTIFICATION_FREQUENCY_STATE

async def store_notification_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Store Notification Frequency")
    text = update.message.text
    freq_map = {'/1hr': 1, '/4hrs': 4, '/12hrs': 12, '/1D': 24}
    
    if text in freq_map:
        context.user_data['notification_frequency'] = freq_map[text]
        logger.info(f"Set notification frequency to {text}")
        await update.message.reply_text(f"You will recieve a notification every {freq_map(text)}hrs")
        set_notifications(update, context)
        show_current_settings(update, context)
        return ENTER_SETTING_STATE
    else:
        logger.error(f"Invalid frequency: {text}")
        await update.message.reply_text("That was not an option. Choose: /1hr, /4hrs, /12hrs, /1D or /back")
        return STORE_NOTIFICATION_FREQUENCY_STATE


async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Exit command")
    return ConversationHandler.END

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Unknown message")
    await update.message.reply_text("Sorry, i have no idea what your saying brev")
    show_current_settings(update, context)
    return ENTER_SETTING_STATE


settings_handler = ConversationHandler(
    entry_points=[CommandHandler("settings", settings_command)],
    states={
        ENTER_SETTING_STATE: [
            CommandHandler("enable_disable", enable_disable),
            CommandHandler("select_sns", select_subnets),
            CommandHandler("notification_frequency", select_notification_frequency),
            CommandHandler("back", exit)
        ],
        STORE_SUBNETS_STATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, store_subnets),
            CommandHandler("back", settings_command)
        ],
        STORE_NOTIFICATION_FREQUENCY_STATE: [
            CommandHandler("1hr", store_notification_frequency),
            CommandHandler("4hrs", store_notification_frequency),
            CommandHandler("12hrs", store_notification_frequency),
            CommandHandler("1D", store_notification_frequency),
            CommandHandler("back", settings_command)
        ],
    },
    fallbacks=[
        CommandHandler("exit", exit),
        '''CommandHandler(filters.TEXT, unknown_message)'''
    ]
)