from telegram.ext import ConversationHandler, CommandHandler

from simple_commands import start_command
from query_alpha_prices import query_netuid_price, enter_alpha_price_commands
from settings import settings_command, select_setting_commands, enter_subnets_commands, select_notification_frequency_commands
from utils import *

select_command_commands = [
    CommandHandler("alpha_prices", query_netuid_price),
    CommandHandler("settings", settings_command)
]


conversation_flow = ConversationHandler(

    entry_points=[
        CommandHandler("start", start_command)
    ],

    states={
        SELECT_COMMAND: select_command_commands,
        ENTER_ALPHA_PRICE: enter_alpha_price_commands,
        SELECT_SETTING: select_setting_commands,
        ENTER_SUBNETS: enter_subnets_commands,
        SELECT_NOTIF_FREQ: select_notification_frequency_commands
    },

    fallbacks=[]
)
