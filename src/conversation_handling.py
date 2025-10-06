from telegram.ext import ConversationHandler, CommandHandler

from simple_commands import *
from query_alpha_prices import query_subnet_price, enter_alpha_price_commands
from settings import *
from utils import *


# Specific commands valid from select command state
select_command_commands = [
    CommandHandler("alpha_prices", query_subnet_price),
    CommandHandler("settings", settings_command)
]


conversation_flow = ConversationHandler(

    # Commands to initiate conversation flow
    entry_points=[
        CommandHandler("start", start_command),
        CommandHandler('show_commands', start_command),
        CommandHandler('help', help_command) # Skips setting up user_data
    ],

    # Different conversation states and their valid specific commands
    states={
        SELECT_COMMAND: select_command_commands,
        ENTER_ALPHA_PRICE: enter_alpha_price_commands,
        SELECT_SETTING: select_setting_commands,
        ENTER_SUBNETS: enter_subnets_commands,
        SELECT_NOTIF_FREQ: select_notification_frequency_commands,
        CUSTOM_NOTIF_FREQ: custom_notification_frequency_commands,
        HELP: select_command_commands + select_setting_commands
    },

    # Commands accessible from all states
    fallbacks=[
        CommandHandler('start', start_command),
        CommandHandler('show_commands', show_commands),
        CommandHandler('help', help_command),
        MessageHandler(filters.COMMAND, unknown_command),
        MessageHandler(filters.TEXT, unknown_message)
    ]
)