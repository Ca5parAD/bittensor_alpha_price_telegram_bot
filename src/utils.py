import logging

from telegram import Update
from telegram.ext import Application, ContextTypes

from config import TOKEN


# Different states in conversation flow
SELECT_COMMAND, ENTER_ALPHA_PRICE, SELECT_SETTING, ENTER_SUBNETS, SELECT_NOTIF_FREQ, CUSTOM_NOTIF_FREQ, HELP = range(7)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Build bot
app = Application.builder().token(TOKEN).build() 


# Populates and sets users notification setings to default
def setup_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Clean up notification job if it still exists
    if context.user_data.get('notification_job'):
        context.user_data['notification_job'].schedule_removal()
        del context.user_data['notification_job']
        
    context.user_data['send_notifications_flag'] = False
    context.user_data['notification_netuids'] = []
    context.user_data['notification_frequency'] = 24

    logger.info(f"user_id:{update.effective_user.id} - settings set to default")