import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler

from utils import ENTER_ALPHA_PRICE, SELECT_COMMAND
from messages import ALPHA_PRICE_MESSAGE
from bittensor_calls import valid_subnets_check, get_netuid_info
from simple_commands import top_level_directions, handle_unknown_message


logger = logging.getLogger(__name__)


async def query_netuid_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("query netuid price")
    await update.message.reply_text(ALPHA_PRICE_MESSAGE)
    return ENTER_ALPHA_PRICE


async def process_netuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("process netuid")


    valid_netuids, invalid_netuids = valid_subnets_check(update.message.text.strip())

    if not valid_netuids:
        await update.message.reply_text(
            "Thats not a valid response\n"
            "Please enter numbers 0-128 seperated ','"
        )
        return ENTER_ALPHA_PRICE

    message = ""

    for i, netuid in enumerate(valid_netuids):
        try:
            netuid_name, netuid_price = get_netuid_info(netuid)
        except Exception as e:
            logger.error(f"Error r: {e}")
            message += f"({i+1}) An error occoured retrieving price, please try again later\n"
        else:
            message += f"({i+1}) {netuid_name} -> {netuid_price}\n"
        
    await update.message.reply_text(message)
    return await query_netuid_price(update, context)



async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Back")
    return await top_level_directions(update, context)



enter_alpha_price_commands = [
    CommandHandler("back", back),
    MessageHandler(filters.TEXT & ~filters.COMMAND, process_netuid),
    MessageHandler(filters.TEXT, handle_unknown_message)
]

