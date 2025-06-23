# core/logger.py
import logging
import os
import sys

def setup_logger(name: str = "JarvisAI", log_file: str = "logs/app.log", level=logging.INFO) -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Console handler with UTF-8 encoding (Windows-safe)
    console_handler = logging.StreamHandler(sys.stdout)
    try:
        console_handler.stream.reconfigure(encoding="utf-8")
    except AttributeError:
        pass  # For Python < 3.7 or terminals that don't support reconfigure
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
