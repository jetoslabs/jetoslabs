from logger import setup_logger, get_logger

setup_logger()
# Logger field name 'app'
logger = get_logger(app="Account")
