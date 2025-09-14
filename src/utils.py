import logging

from telegram import Update
from telegram.ext import Application, ContextTypes

from config import TOKEN

logger = logging.getLogger(__name__)

# States
SELECT_COMMAND, ENTER_ALPHA_PRICE, SELECT_SETTING, ENTER_SUBNETS, SELECT_NOTIF_FREQ, CUSTOM_NOTIF_FREQ, HELP = range(7)


# Build bot
app = Application.builder().token(TOKEN).build() 

def reset_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('notification_job'):
        context.user_data['notification_job'].schedule_removal()
        del context.user_data['notification_job'] # Clean up notification job
        
    context.user_data['send_notifications_flag'] = False
    context.user_data['notification_subnets'] = []
    context.user_data['notification_frequency'] = 24

    logger.info(f"user_id:{update.chat.id} - settings set to default")