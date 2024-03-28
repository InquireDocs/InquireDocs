import logging

from app.core.config import settings

# Set up logging configuration
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Configure the console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# Configure the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
root_logger.addHandler(console_handler)

# Import this in other modules to use the configured logger
logger = logging.getLogger(__name__)

# Print effective level for root logger
effective_level = root_logger.getEffectiveLevel()
logger.info("Root logger effective level %s", logging.getLevelName(effective_level))
