# Centralized logger for the assistant
import logging
import os

def setup_logger(name: str = "JarvisAI", log_file: str = "logs/app.log", level=logging.INFO) -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent multiple handlers from being added repeatedly
    if not logger.hasHandlers():
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger
