import logging


def setup_root_logger(log_file="basic_bot.log") -> None:
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # File handler for all levels
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(file_handler)

    # Stream handler for all levels
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(stream_handler)

    # Explicitly set levels for our modules
    logging.getLogger('start').setLevel(logging.DEBUG)
    logging.getLogger('query_subnet_price').setLevel(logging.DEBUG)
    logging.getLogger('settings').setLevel(logging.DEBUG)
    logging.getLogger('help').setLevel(logging.DEBUG)


    




