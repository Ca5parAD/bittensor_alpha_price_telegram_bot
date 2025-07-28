from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sys
sys.path.append('')
import bittensor

TOKEN: Final = ''
BOT_USERNAME: Final = ''

subtensor = bittensor.subtensor(network='finney')

def get_alpha_price(netuid: int) -> float:
    subnet_info = subtensor.subnet(netuid)
    return subnet_info.price

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there')

async def get_alpha_price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What SN price would you like to know? (reply with just the number)')
    # Store a flag to indicate we're expecting a netuid response
    context.user_data['awaiting_netuid'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_netuid', False):
        text: str = update.message.text
        try:
            netuid = int(text.strip())
            alpha_price = get_alpha_price(netuid)
            await update.message.reply_text(f'SN {netuid}\'s price is: {alpha_price}')
            # Reset the flag after processing
            context.user_data['awaiting_netuid'] = False
        except ValueError:
            await update.message.reply_text('Please provide a valid number.')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('alpha_prices', get_alpha_price_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Polling...')
    app.run_polling(poll_interval=3)