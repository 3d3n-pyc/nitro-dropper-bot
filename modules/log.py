import logging

LEVEL_COLOURS = [
    (logging.DEBUG, '\x1b[40;1m'),
    (logging.INFO, '\x1b[34;1m'),
    (logging.WARNING, '\x1b[33;1m'),
    (logging.ERROR, '\x1b[31m'),
    (logging.CRITICAL, '\x1b[41m'),
]

FORMATS = {
    level: logging.Formatter(
        f'\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s',
        '%Y-%m-%d %H:%M:%S',
    )
    for level, colour in LEVEL_COLOURS
}

def setup(name, level=logging.DEBUG):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(FORMATS.get(level, logging.Formatter()))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def debug(logger, message):
    logger.debug(message)

def info(logger, message):
    logger.info(message)

def warning(logger, message):
    logger.warning(message)

def error(logger, message):
    logger.error(message)

def critical(logger, message):
    logger.critical(message)

