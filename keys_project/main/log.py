import logging

# log_format = '[%(asctime)s] :: [%(name)s] :: [%(levelname)s] :: [FN = %(funcName)s] :: [%(message)s]'
log_format = '[%(asctime)s] :: [%(name)s] :: [FN = %(funcName)s] :: %(message)s'


def get_debug_logger(log_name, print=False):
    debug_logger = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    if print:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        debug_logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('logs/debug.log', mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    debug_logger.addHandler(file_handler)

    debug_logger.setLevel(logging.DEBUG)

    return debug_logger


def get_info_logger(log_name, print=False):
    info_logger = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    if print:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        info_logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('logs/info.log', mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)
    info_logger.addHandler(file_handler)

    info_logger.setLevel(logging.INFO)

    return info_logger


def get_err_logger(log_name, print=False):
    err_logger = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    if print:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        err_logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('logs/errors.log', mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.ERROR)
    err_logger.addHandler(file_handler)

    err_logger.setLevel(logging.ERROR)

    return err_logger
