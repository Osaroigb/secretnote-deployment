import os
import logging
from dotenv import load_dotenv
from colorlog import ColoredFormatter

# Load environment variables from .env file
load_dotenv()

# Constants for environment variable names
HOST_VAR = "HOST"
PORT_VAR = "PORT"
WHAT3WORDS_API_KEY_VAR = "WHAT3WORDS_API_KEY"

# Configuration class
class Config:
    HOST: str = os.getenv(HOST_VAR)
    PORT: int = int(os.getenv(PORT_VAR))
    WHAT3WORDS_API_KEY: str = os.getenv(WHAT3WORDS_API_KEY_VAR)

    @classmethod
    def validate_env(cls):
        required_vars = [
            HOST_VAR,
            PORT_VAR,
            WHAT3WORDS_API_KEY_VAR
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Define color format for log messages
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
    },
)

# Set up logging with color formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])