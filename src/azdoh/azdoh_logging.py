import logging
from colorlog import ColoredFormatter

# From https://stackoverflow.com/a/23964880
LOGFORMAT = "%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"


def initialize_logger(loglevel: str):
    formatter = ColoredFormatter(LOGFORMAT)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)
    logging.basicConfig(level=loglevel, handlers=[handler])
