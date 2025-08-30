import logging
import sys
import traceback


from telegram import Update
from telegram.ext import Application, ContextTypes, _contexttypes

from logger_config import setup_root_logger
from utils import app
from config import TOKEN, BOT_USERNAME
from start import start_handler
from help import help_handler
from query_subnet_price import query_netuid_price_handler
from settings import notification_settings_handler


setup_root_logger()
logger = logging.getLogger(__name__)


# Error handler: log short message to file, print full traceback to terminal if WARNING+
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Log short error message to file (INFO+)
    logger.exception(f"Update caused error: {context.error}")
    # Print traceback to terminal if error is WARNING or higher
    if hasattr(context, 'error') and context.error:
        print(f"\n[ERROR] Update: {update}\nError: {context.error}")
        traceback.print_exception(type(context.error), context.error, context.error.__traceback__)


if __name__ == '__main__':
    # Test log to verify logging setup (should appear in log file if level is set correctly)
    logger.info("program started")

    # Register command handlers for the bot
    app.add_handler(start_handler)  # /start command
    app.add_handler(query_netuid_price_handler)  # /alpha_price command
    app.add_handler(notification_settings_handler)  # /notification_settings command
    app.add_handler(help_handler)  # /help command

    # Register global error handler for uncaught exceptions in handlers
    app.add_error_handler(error)

    # Start polling for new updates from Telegram
    logger.info('polling...')
    app.run_polling()
