from telegram.ext import Application
from config import TOKEN

# Build bot
app = Application.builder().token(TOKEN).build() 