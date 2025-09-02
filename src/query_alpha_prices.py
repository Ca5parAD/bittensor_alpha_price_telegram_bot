import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler

from utils import ENTER_ALPHA_PRICE, SELECT_COMMAND
from messages import ALPHA_PRICE_MESSAGE
from bittensor_calls import get_netuid_info
from simple_commands import top_level_directions, handle_unknown_message


logger = logging.getLogger(__name__)


async def query_netuid_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("query netuid price")
    await update.message.reply_text(ALPHA_PRICE_MESSAGE)
    return ENTER_ALPHA_PRICE


async def process_netuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("process netuid")
    netuid = int(update.message.text.strip())
    logger.debug(f"Netuid -> {netuid}")
    if 0 <= netuid <= 128:
        try:
            netuid_name, netuid_price = get_netuid_info(netuid)
        except Exception as e:
            logger.error(f"Error r: {e}")
            await update.message.reply_text("An error occoured retrieving price, please try again later")
        else:
            await update.message.reply_text(f"{netuid_name} -> {netuid_price}")
        finally:
            return await query_netuid_price(update, context)

    else:
        await update.message.reply_text("Thats not a valid response, please enter a number 0-128")
        return ENTER_ALPHA_PRICE


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Back")
    return await top_level_directions(update, context)



enter_alpha_price_commands = [
    CommandHandler("back", back),
    MessageHandler(filters.TEXT & ~filters.COMMAND, process_netuid),
    MessageHandler(filters.TEXT, handle_unknown_message)
]

