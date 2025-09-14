from typing import Final

# Simple Commands Messages
START_MESSAGE: Final = (
    "<b>Welcome to the Bittensor Subnet Bot!</b> 👋"
)

SHOW_COMMANDS_MESSAGE: Final = (
    "📈 Check alpha prices: /alpha_prices\n\n"
    "⚙️ Manage notifications: /settings\n\n"
    "❓ Need guidance: /help"
)

HELP_MESSAGE: Final = (
    "<b>Bittensor Subnet Bot Help Menu</b> 🆘\n\n"
    "• /alpha_prices: Check alpha prices for subnets (0-128) 📈\n\n"
    "• /settings: Customize notifications ⚙️\n"
    "   - /enable_disable: Toggle alerts on/off 🔔/🔕\n"
    "   - /select_sns: Pick subnets to track 📌\n"
    "   - /notification_frequency: Set update intervals (hourly, daily) ⏰\n\n"
    "• /help: Show this menu anytime ❓\n\n"
    "• /back: To go back to the home menu 🏠\n\n"
    "• /start: To reset settings and restart conversation flow 🔄\n\n"
    "Settings are saved per user. Notifications include quick links to keep your flow smooth! 😊"
)

# Query Alpha Prices Messages
ALPHA_PRICE_MESSAGE: Final = (
    "<b>Check Subnet Alpha Prices</b> 📈\n\n"
    "Enter the netuid(s) you want:\n"
    "• Single: e.g. '19' 🔢\n"
    "• Multiple: e.g. '19,56,64' 📋\n\n"
    "• /my_sns: See your tracked subnets 📌\n\n"
    "• /back: Return to main menu ↩️"
)

INVALID_PROCESS_NETUID: Final = (
    "<b>Invalid Input</b> ❌\n\n"
    "Please enter numbers 0-128 separated by commas - e.g. '19, 56, 64'\n\n"
    "Use /back to go back ↩️\n"
)

# Settings Messages
SETTINGS_COMMANDS_MESSAGE: Final = (
    "• /enable_disable: Toggle alerts on/off 🔔/🔕\n"
    "• /select_sns: Choose subnets to track 📌\n"
    "• /notification_frequency: Set notification frequency ⏰\n"
    "• /back: Back to main menu ↩️"
)

SELECT_SUBNETS_MESSAGE: Final = (
    "<b>Select Subnets to Track</b> 📌\n\n"
    "Enter netuids separated by commas - e.g. '19,56,64' 🔢.\n\n"
    "/back: Back to settings ↩️"
)

SELECT_NOTIFICATION_FREQUENCY_MESSAGE: Final = (
    "<b>Set Notification Frequency</b> ⏰\n\n"
    "Choose how often you want updates:\n"
    "• /1hr: Every hour 🕐\n"
    "• /4hrs: Every 4 hours 🕓\n"
    "• /12hrs: Every 12 hours 🕕\n"
    "• /1D: Daily 📅\n"
    "• /custom: For a custom interval\n\n"
    "/back: Back to settings ↩️"
)

INVALID_NOTIFICATION_FREQUENCY: Final = (
    "<b>Invalid Input</b> ❌\n\n"
    "Please choose: /1hr, /4hrs, /12hrs, /1D, /custom.\n\n"
    "Use /back to go back ↩️\n"
)

# ****************************
CUSTOM_NOTIFICATION_FREQUENCY_MESSAGE: Final = (
    "<b>Custom Notification Frequency</b> ⏰\n\n"
    "Enter your notification interval in hours\n\n"
    "/back: Back to notification frequency ↩️"
)

# Unkowns Messages
UNKNOWN_COMMAND: Final = (
    "❌ That's not a valid command\n"
    "Please try again\n\n"
    "Or use /back to go back ↩️\n"
)

UNKNOWN_MESSAGE: Final = (
    "🤔 I'm not sure what you meant - I'm probably expecting a command\n\n"
    "Please try again\n\n"
    "Or use /back to go back ↩️\n"
)

OUTSIDE_CONVERSATION_MESSAGE: Final = (
    "❌ Sorry, you are not in a conversation\n"
    "Use /start to start"
)
