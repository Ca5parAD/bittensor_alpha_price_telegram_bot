import logging

from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler, ConversationHandler

from messages import ALPHA_PRICE_MESSAGE
from bittensor_calls import get_netuid_info


logger = logging.getLogger(__name__)

ENTER_NETUID_STATE = 1 # Conversation state for netuid entry user input


async def query_netuid_price_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Query netuid price conversation started")
    await update.message.reply_text(ALPHA_PRICE_MESSAGE)
    return ENTER_NETUID_STATE

async def process_netuid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    netuid = int(update.message.text.strip())
    if 0 <= netuid <= 128:
        try:
            netuid_name, netuid_price = get_netuid_info(netuid)
        except Exception as e:
            logger.error(f"Error r: {e}")
            await update.message.reply_text("An error occoured retrieving price, please try again later")
        else:
            await update.message.reply_text(f"{netuid_name}: {netuid_price}")
        finally:
            return ConversationHandler.END

    else:
        await update.message.reply_text("Thats not a valid response, please enter a number 0-128")
        return ENTER_NETUID_STATE


async def query_notification_subnets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Query notification subnets")
    await update.message.reply_text("Bittensor loop for your SNs")
    return ENTER_NETUID_STATE


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Back")
    return ConversationHandler.END

query_netuid_price_handler = ConversationHandler(
    entry_points=[CommandHandler("alpha_price", query_netuid_price_entry)],
    states={ENTER_NETUID_STATE: [
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_netuid),
        CommandHandler("my_sns", query_notification_subnets)
        ]
    },
    fallbacks=[CommandHandler("back", back)],
)

