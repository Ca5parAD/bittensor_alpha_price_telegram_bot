import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler

from utils import ENTER_ALPHA_PRICE
from messages import ALPHA_PRICE_MESSAGE, INVALID_PROCESS_NETUIDS
from simple_commands import show_commands
from taostats_calls import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def query_subnet_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to input or select which alpha prices to query"""
    logger.info(f"user_id:{update.message.chat.id} - query subnet price")
    await update.message.reply_text(ALPHA_PRICE_MESSAGE, parse_mode="HTML")
    return ENTER_ALPHA_PRICE

async def process_netuids(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process text into netuids and send prices message to user"""
    logger.info(f"user_id:{update.message.chat.id} - process netuid")
    text = update.message.text.strip() # Store user input
    logger.debug(f"user_id:{update.message.chat.id} - user input: {text}")

    try: # Check validity of user response
        valid_subnets, invalid_netuids = valid_netuids_check(text)
 
    except ValueError as e: # Does this need to specify ValueError? # Show user message if invalid
        logger.debug(f"user_id:{update.message.chat.id} - invalid input: {text} - {str(e)}")
        await update.message.reply_text(INVALID_PROCESS_NETUIDS, parse_mode="HTML")
        return ENTER_ALPHA_PRICE  # Stay in state for retry
    
    else:
        # Message to user for invalid netuids
        if invalid_netuids:
            invalid_netuids_message = "⚠️ Invalid netuid(s):\n"
            for netuid in invalid_netuids:
                invalid_netuids_message += f"{netuid}\n"
                await update.message.reply_text(invalid_netuids_message)

        message = "<b>Alpha Prices</b> 📈\n"

        try:
            subnets_info_text = get_subnets_info_text(valid_subnets)

        except Exception as e:
            logger.error(
                f"user_id:{context.job.chat_id} - API call failed: {e}",
                exc_info=True
            )
            message += "Failed to connect to tao stats 😓\n\n"

        else:
            message += subnets_info_text

        await update.message.reply_text(message, parse_mode="HTML")
        return await show_commands(update, context)

async def my_sns(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send prices message of selected subnets to user"""
    logger.info(f"user_id:{update.message.chat.id} - query 'my sns'")
    subnets = context.user_data.get('notification_subnets', [])
    message = "<b>Alpha Prices</b> 📈\n"
    if not subnets:
        message += "No subnets selected ❌.\n"
    else:
        try:
            subnets_info_text = get_subnets_info_text(subnets)

        except Exception as e:
            logger.error(
                f"user_id:{context.job.chat_id} - API call failed: {e}",
                exc_info=True
            )
            message += "Failed to connect to tao stats 😓\n\n"

        else:
            message += subnets_info_text
    
    await update.message.reply_text(message, parse_mode="HTML")
    return await show_commands(update, context)


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Goes back to main menu"""
    logger.info(f"user_id:{update.message.chat.id} - back")
    return await show_commands(update, context)


# Valid specific commands per state
enter_alpha_price_commands = [
    CommandHandler('my_sns', my_sns),
    CommandHandler('back', back),
    MessageHandler(filters.TEXT & ~filters.COMMAND, process_netuids)
]