import logging
from . import my_logger

def getLogger(module_name:str, loglevel=logging.DEBUG):
    module_logger = my_logger.get_logger(module_name, loglevel=loglevel)
    return module_logger

logger = getLogger(__name__)