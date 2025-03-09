import logging
from logging.handlers import RotatingFileHandler
import time

def setup_logger():
    """
    Sets up a logger with both file and console handlers.

    The logger writes INFO level messages to:
    - A rotating file ("app.log") with a maximum size of 1MB and 5 backup files.
    - The console (stdout).

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a rotating file handler
    file_handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=5)
    file_handler.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def log_usage_data(model_used, token_count, cost, time_taken, success):
    """
    Logs usage data for a model request.

    Args:
        model_used (str): The name of the model used.
        token_count (int): The number of tokens used.
        cost (float): The cost of the request in Rupees.
        time_taken (float): The time taken to process the request in seconds.
        success (bool): Whether the request was successful.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Model: {model_used}, Tokens: {token_count}, Cost: Rs {cost:.4f}, Time: {time_taken:.2f}s, Success: {success}")

#Example usage
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Application started.")
    log_usage_data("GPT-3", 100, 0.50, 1.23456, True)
    logger.info("Application finished.")