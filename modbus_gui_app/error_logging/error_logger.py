import logging


def init_logger(name):
    up_line = "===================================================================================================\n"
    f = up_line + '%(asctime)s \n %(message)s'
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format=f)
    logger = logging.getLogger(name)
    return logger
