
import logging
import os
import sys

os.makedirs('logs', exist_ok=True)

# Formatter with time, logger name, level, and message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a stream handler that outputs to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.captureWarnings(True)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

logger.addHandler(console_handler)
