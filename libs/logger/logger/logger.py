import sys

from loguru import logger


def setup_logger():
    logger.remove(0)
    logger.add(sys.stderr,
               level='DEBUG',
               format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{extra}</level> - <yellow>{message}</yellow>",
               colorize=True,
               serialize=False)


def get_logger(**kwargs) -> logger:
    log = logger.bind(**kwargs)
    return log


def get_child_logger(parent_logger: logger, **kwargs) -> logger:
    log = parent_logger.bind(**kwargs)
    return log
