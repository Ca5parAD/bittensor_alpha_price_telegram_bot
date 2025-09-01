from telegram.ext import Application
from config import TOKEN

SELECT_COMMAND, ENTER_ALPHA_PRICE, SELECT_SETTING, ENTER_SUBNETS, SELECT_NOTIF_FREQ = range(5)


# Build bot
app = Application.builder().token(TOKEN).build() 