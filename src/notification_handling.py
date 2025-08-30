import logging

from telegram import Update
from telegram.ext import Application, ContextTypes

from utils import app

async def set_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data['send_notifications_flag']:
        interval_s = context.user_data['notification_frequency'] * 60 ** 2
        app.job_queue.run_repeating(
            send_notification,
            chat_id=update.effective_message.chat_id,
            interval=interval_s,
            first=interval_s,
            data=update.effective_message.chat_id
        )


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    message = "Current Subnets:\n"
    for i, netuid in enumerate(context.user_data['notification_subnets']):
        message.append(f"{i}. {netuid}\n")

    await context.bot.send_message(chat_id=context.job.chat_id, text=message)

    pass