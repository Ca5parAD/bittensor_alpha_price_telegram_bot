import logging
import asyncio

from logger_config import setup_root_logger
from data_persistance import initialise_from_database
from utils import app
from conversation_handling import conversation_flow
from simple_commands import outside_conversation_handler, error


setup_root_logger()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def main():
    logger.info("program started")
    await initialise_from_database()
    
    app.add_handler(conversation_flow)
    app.add_handler(outside_conversation_handler) # Catches commands outside of conversation flow
    app.add_error_handler(error)
    
    # Starts program polling
    await app.initialize()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == '__main__':
    asyncio.run(main())