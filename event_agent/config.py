"""Config module for Eventbrite Agent"""
import logging
import sys

# Eventbrite API token
EVENTBRITE_TOKEN = "VFRIC7C7O57WTRNPWFGE"


def setup_logging(level=logging.INFO):
    """Logging setup (centralized)."""
    logger = logging.getLogger()
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)

setup_logging()
