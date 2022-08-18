import logging
from functools import lru_cache


class CustomFormatter(logging.Formatter):
    """
    The class is used to change the logging format.
    Logs are not colored by default (can be passed via :param colorize)
    """

    def __init__(self, handler_format, colorize):
        super().__init__()
        self.handler_format = handler_format
        self.colorize = colorize
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        if not colorize:
            formats = {
                logging.DEBUG: self.handler_format,
                logging.INFO: self.handler_format,
                logging.WARNING: self.handler_format,
                logging.ERROR: self.handler_format,
                logging.CRITICAL: self.handler_format
            }
        else:

            formats = {
                logging.DEBUG: grey + self.handler_format + reset,
                logging.INFO: grey + self.handler_format + reset,
                logging.WARNING: yellow + self.handler_format + reset,
                logging.ERROR: red + self.handler_format + reset,
                logging.CRITICAL: bold_red + self.handler_format + reset
            }
        self.formats = formats

    def format(self, record) -> str:
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    """
    Class for creating a logger.
    :param name: Selecting a logger name.
    :param ko_logger_level: Logger level selection.
    :param handler_format: Changing the logger format.
    (LogRecord attributes) Uses string https://docs.python.org/3/library/logging.html#logrecord-attributes .
    :param colorize: Selects whether the logs will be colored.
    True - colorize (Logs may not display correctly. For example, in Grafana when viewing logs).
    False - Default.
    :param set_handlers_format: Changing the format of handlers.
    'all' - change them all.
    [uvicorn, loggername2] - you can pass a list with names to change them.
    """

    def __init__(self, name: str = 'ko_logger', ko_logger_level: logging = logging.DEBUG,
                 handler_format: str = "[%(name)s] [%(process)s] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s",
                 colorize: bool = False, set_handlers_format: str | tuple = "all"):
        self.ko_logger = logging.getLogger(name)
        self.custom_handler = logging.StreamHandler()
        self.ko_logger.setLevel(ko_logger_level)
        self.ko_logger.addHandler(self.custom_handler)
        if set_handlers_format == "all":
            for name in logging.root.manager.loggerDict:
                default_logger = logging.getLogger(name)
                default_logger.handlers = self.ko_logger.handlers
                for handler in default_logger.handlers:
                    handler.setFormatter(CustomFormatter(handler_format, colorize))
        if type(set_handlers_format) is tuple:
            for name in set_handlers_format:
                default_logger = logging.getLogger(name)
                default_logger.handlers = self.ko_logger.handlers
                for handler in default_logger.handlers:
                    handler.setFormatter(CustomFormatter(handler_format, colorize))
        self.ko_logger.info(
            f'Logger "{self.ko_logger.name}" has been created. logger.level={self.ko_logger.level}')


@lru_cache
def get_logger(name='ko_logger', ko_logger_level=logging.DEBUG,
               handler_format="[%(name)s] [%(process)s] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s",
               colorize=False, set_handlers_format="all"):
    return Logger(**locals()).ko_logger
