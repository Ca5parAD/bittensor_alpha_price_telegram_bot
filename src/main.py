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
    # Initialize database first
    await initialise_from_database()
    
    # Set up handlers
    app.add_handler(conversation_flow)
    app.add_handler(outside_conversation_handler)
    app.add_error_handler(error)
    
    # Start the bot using built-in runner which handles event loop correctly
    await app.run_polling()

if __name__ == '__main__':
    # This runs everything in a single event loop
    asyncio.run(main())