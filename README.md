# Bittensor-Alpha-Price-Telegram-Bot

A telegram bot for allowing users to query the performance of bittensor subnet prices, as well as the option to recieve repetitive notification updates on the performance of their selected subnets.

<img src="https://github.com/Ca5parAD/bittensor_alpha_price_telegram_bot/blob/main/Images/alpha_prices.jpg?raw=true" alt="alpha_prices" height="380"> <img src="https://github.com/Ca5parAD/bittensor_alpha_price_telegram_bot/blob/main/Images/settings%20command.jpg?raw=true" alt="settings" height="380"> <img src="https://github.com/Ca5parAD/bittensor_alpha_price_telegram_bot/blob/main/Images/notifications.jpg?raw=true" alt="notifications" height="380">

### Prerequisites

- Python 3.9+
- Telegram api bot token
> [!NOTE]
> - Use [BotFather](https://telegram.me/BotFather) to gain an API key


### Dependencies

Installation of the dependencies will be covered in the below **Installation** section
```py
bittensor==9.10.1
python-telegram-bot[job-queue]==22.4
```


## Installation

To install the program and its necessary dependencies:

1. Clone the repository
```bash
git clone https://github.com/Ca5parAD/bittensor_alpha_price_telegram_bot
cd bittensor_alpha_price_telegram_bot
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```


## Setup

To get the bot up and run you must first edit the config file (src/config.py) to include your API key and the path to your log file

```py
TOKEN = "123..."

LOG_FILE_PATH = "/path/to/log/file/bot.log"
```

> [!IMPORTANT]
> The path to the log file must include the log file itself: /bot.log (or your preference)

The bot is now ready to run:
```bash
python main.py
```


## Usage

Usage of the bot is intuative, with sub-commands under each of these:
- **/start** is used to start the bot, or at any time can reset user settings
- **/alpha_prices** can be used to query alpha prices

 

  
- **/settings** is used to set notification settings
  
- **/help** shows a full description of bot commands and navigation


## Contributing

Contributions welcome! Open an issue or submit a pull request


## License

MIT License (LICENSE)
