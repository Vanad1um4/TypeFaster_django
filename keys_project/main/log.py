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


def get_crit_logger(log_name, print=False):
    crit_logger = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    if print:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        crit_logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('logs/critical.log', mode='a')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.CRITICAL)
    crit_logger.addHandler(file_handler)

    crit_logger.setLevel(logging.CRITICAL)

    return crit_logger
