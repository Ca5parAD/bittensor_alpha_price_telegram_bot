import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler

from utils import ENTER_ALPHA_PRICE, SELECT_COMMAND
from messages import ALPHA_PRICE_MESSAGE, INVALID_PROCESS_NETUID
from bittensor_calls import valid_subnets_check, get_netuid_info
from simple_commands import show_commands, show_commands_handler


logger = logging.getLogger(__name__)


async def query_netuid_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("query netuid price")
    await update.message.reply_text(ALPHA_PRICE_MESSAGE, parse_mode="HTML")
    return ENTER_ALPHA_PRICE


async def process_netuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("process netuid")
    logger.debug(f"user input: {update.message.text}")
    valid_netuids, invalid_netuids = valid_subnets_check(update.message.text.strip())

    if not valid_netuids:
        await update.message.reply_text(INVALID_PROCESS_NETUID, parse_mode="HTML")
        return ENTER_ALPHA_PRICE

    message = "<b>Subnet Prices</b> 📈\n"

    for i, netuid in enumerate(valid_netuids):
        try:
            netuid_name, netuid_price = get_netuid_info(netuid)
        except Exception as e:
            logger.warning(f"Error retrieving netuid {netuid}: {e}")
            message += f"({netuid}) Error retrieving price ⚠️\n"
        else:
            message += f"({netuid}) {netuid_name}: {netuid_price}\n"
        
    await update.message.reply_text(message, parse_mode="HTML")
    return await show_commands(update, context)


async def my_sns(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("my sns")
    message = "<b>Subnet Prices</b> 📈\n"

    subnets = context.user_data.get('notification_subnets', [])
    if not subnets:
        message += "No subnets selected 📌.\n"
    else:
        for i, netuid in enumerate(subnets):
            try:
                netuid_name, netuid_price = get_netuid_info(netuid)
                message += f"({netuid}) {netuid_name}: {netuid_price}\n"
            except Exception as e:
                logger.warning(f"Error retrieving netuid {netuid}: {e}")
                message += f"({netuid}) Error retrieving price ⚠️\n"

    await update.message.reply_text(message, parse_mode="HTML")
    return await show_commands(update, context)


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info('Back')
    return await show_commands(update, context)


enter_alpha_price_commands = [
    CommandHandler('my_sns', my_sns),
    CommandHandler('back', back),
    MessageHandler(filters.TEXT & ~filters.COMMAND, process_netuid),
    show_commands_handler                   
]

