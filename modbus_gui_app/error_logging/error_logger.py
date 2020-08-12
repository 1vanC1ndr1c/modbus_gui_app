import logging


def init_logger(name):
    """A function used to make an instance of a logging.logger with the specified name.

    Args:
        name(str): A logger name to be specified  or, if name is None,
                    return a logger which is the root logger of the hierarchy.

    Returns:
        logging.logger: Returns an instance of a logger.

    """
    up_line = "===================================================================================================\n"
    f = up_line + '%(asctime)s \n %(message)s'
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format=f)
    logger = logging.getLogger(name)
    return logger
