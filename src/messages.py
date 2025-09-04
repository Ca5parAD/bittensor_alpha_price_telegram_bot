from typing import Final

START_MESSAGE: Final = (
    "Welcome to the Bittensor Subnet Bot!"
)

TOP_LEVEL_DIRECTIONS_MESSAGE: Final = (
    "Get alpha prices with /alpha_prices\n\n"
    "Manage notifications with /settings\n\n"
    "Or use /help for more details"
)

HELP_MESSAGE: Final  = (
    "Bittensor Subnet Bot Help:\n\n"
    "- /start: Displays initial welcome message\n\n"
    "- /alpha_prices: Query the alpha price of a Bittensor subnet (0-128)\n\n"
    "- /settings: Manage notification settings:\n"
    "   - /enable_disable: Turn notifications on or off\n"
    "   - /select_sns: Specify subnet IDs to track\n"
    "   - /notification_frequency: Set how often to receive updates\n"
    "   - /back: Go back\n\n"
    "- /help: Displays this help message\n\n"
    "Use commands to navigate. All settings are saved per user"
)

ALPHA_PRICE_MESSAGE: Final = (
    "What subnet price(s) would you like to know?:\n"
    "- For a single SN enter its netuid\n"
    "- For multiple netuids use a comma to seperate\n"
    "- /my_sns to check your chosen SNs\n"
    "- /back to go back"
)

SETTINGS_COMMANDS_MESSAGE: Final = (
    "What would you like to change?:\n"
    "- /enable_disable to toggle notifications\n"
    "- /select_sns to choose subnets\n"
    "- /notification_frequency to set frequency\n"
    "- /back"
)

SELECT_SUBNETS_MESSAGE: Final = (
    "What subnets would you like to track?:\n"
    "Enter the netuids seperated by ', '\n"
    "e.g. '19, 56, 64'"
)

SELECT_NOTIFICATION_FREQUENCY_MESSAGE: Final = (
    "How often would you like to recieve alerts?:\n"
    "/1hr\n"
    "/4hrs\n"
    "/12hrs\n"
    "/1D\n\n"
    "/back to go back"
)

UNKOWN_MESSAGE_MESSAGE: Final = ("Sorry, I don't know what you mean - I am likely expecting a command")

UNKOWN_COMMAND_MESSAGE: Final = ("That's not a valid command")




'''

need to work out how notifications handle interrupting conversation flow
notifications give command for easy navigation


'''