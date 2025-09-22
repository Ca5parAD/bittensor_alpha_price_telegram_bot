import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler

from utils import ENTER_ALPHA_PRICE
from messages import ALPHA_PRICE_MESSAGE, INVALID_PROCESS_NETUID
from bittensor_calls import *
from simple_commands import show_commands


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def query_netuid_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.message.chat.id} - query netuid price (alpha price command)")
    await update.message.reply_text(ALPHA_PRICE_MESSAGE, parse_mode="HTML")
    return ENTER_ALPHA_PRICE


async def process_netuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.message.chat.id} - store subnets")
    text = update.message.text.strip()
    logger.debug(f"user_id:{update.message.chat.id} - user input: {text}")

    try:
        valid_netuids, invalid_netuids = valid_netuids_check(text)
 
    except ValueError as e: # Does this need to specify ValueError?
        logger.debug(f"user_id:{update.message.chat.id} - invalid input: {text} - {str(e)}")
        await update.message.reply_text(INVALID_PROCESS_NETUID, parse_mode="HTML")
        return ENTER_ALPHA_PRICE  # Stay in state for retry
    
    else:
        if invalid_netuids:
            invalid_netuids_message = "⚠️ Invalid subnet(s):\n"
            for netuid in invalid_netuids:
                invalid_netuids_message += f"{netuid}\n"
                await update.message.reply_text(invalid_netuids_message)

        message = "<b>Subnet Prices</b> 📈\n"
        info_obj = GetNetuidInfoObj
        for netuid in valid_netuids:
            try:
                netuid_name, netuid_price = info_obj.get_netuid_info(netuid)
            except Exception as e:
                logger.warning(f"user_id:{update.message.chat.id} - Error retrieving netuid {netuid}: {e}")
                message += f"({netuid}) Error retrieving price ⚠️\n"
            else:
                message += f"({netuid}) {netuid_name}: {netuid_price}\n"

        info_obj.close()
            
        await update.message.reply_text(message, parse_mode="HTML")
        return await show_commands(update, context)


async def my_sns(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.message.chat.id} - query 'my sns'")
    message = "<b>Subnet Prices</b> 📈\n"

    subnets = context.user_data.get('notification_netuids', [])
    if not subnets:
        message += "No subnets selected 📌.\n"
    else:
        info_obj = GetNetuidInfoObj
        for netuid in subnets:
            try:
                netuid_name, netuid_price = info_obj.get_netuid_info(netuid)
                message += f"({netuid}) {netuid_name}: {netuid_price}\n"
            except Exception as e:
                logger.warning(f"user_id:{update.message.chat.id} - Error retrieving netuid {netuid}: {e}")
                message += f"({netuid}) Error retrieving price ⚠️\n"

        info_obj.close()
        await update.message.reply_text(message, parse_mode="HTML")

    return await show_commands(update, context)


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"user_id:{update.message.chat.id} - back")
    return await show_commands(update, context)


enter_alpha_price_commands = [
    CommandHandler('my_sns', my_sns),
    CommandHandler('back', back),
    MessageHandler(filters.TEXT & ~filters.COMMAND, process_netuid)
]

