import logging
import os


def get_logger(file_name):
    """
    :param file_name: Name file
    :return: Logger object
    """
    logger_name = os.path.basename(file_name).split('.')[0]
    logger = logging.getLogger(logger_name.upper())
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

    return logger
