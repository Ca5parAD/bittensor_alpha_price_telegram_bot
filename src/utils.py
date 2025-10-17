import logging

from telegram.ext import Application

from config import TELEGRAM_BOT_TOKEN


# Different states in conversation flow
SELECT_COMMAND, ENTER_ALPHA_PRICE, SELECT_SETTING, ENTER_SUBNETS, SELECT_NOTIF_FREQ, CUSTOM_NOTIF_FREQ, HELP = range(7)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Build bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build() 