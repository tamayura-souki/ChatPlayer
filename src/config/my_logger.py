import logging

def get_logger(modname, loglevel=logging.DEBUG):
    logger  = logging.getLogger(modname)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    logger.setLevel(loglevel)
    logger.addHandler(handler)
    logger.propagate = False

    return logger