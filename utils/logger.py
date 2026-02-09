import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = "app.log"
# Create logs folder if not exists
os.makedirs(LOG_DIR, exist_ok=True)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Create rotating file handler
file_handler = TimedRotatingFileHandler(
    LOG_PATH,
    when="D",          # Rotate daily
    interval=1,        # Every 1 day
    backupCount=30,    # Keep logs for last 30 days
    encoding="utf-8"
)

# Log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Root logger config
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

def get_logger(name: str):
    return logging.getLogger(name)