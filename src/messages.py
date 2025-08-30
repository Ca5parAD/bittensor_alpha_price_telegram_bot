from typing import Final

START_MESSAGE: Final = (
    "Welcome to the Bittensor Subnet Bot! Get alpha prices with /alpha_price "
    "or manage notifications with /notification_settings. Use /help for details."
)

HELP_MESSAGE: Final  = (
    "Bittensor Subnet Bot Help:\n\n"
    "- /start: Displays initial welcome message\n\n"
    "- /alpha_price: Query the alpha price of a Bittensor subnet (0-128)\n\n"
    "- /notification_settings: Manage notification settings:\n"
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
    "- /back to exit conversation"
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
    "/1D"
)