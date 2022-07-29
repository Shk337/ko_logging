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
    :param logger_name: Selecting a logger name.
    :param logger_level: Logger level selection.
    :param format_handler: Changing the logger format.
    (LogRecord attributes) Uses string https://docs.python.org/3/library/logging.html#logrecord-attributes .
    :param color: Selects whether the logs will be colored.
    True - colorize (Logs may not display correctly. For example, in Grafana when viewing logs).
    False - Default.
    :param set_handlers_format: Changing the format of handlers.
    'all' - change them all.
    [uvicorn, loggername2] - you can pass a list with names to change them.
    """

    def __init__(self, logger_name='ko_logging', logger_level=logging.DEBUG,
                 format_handler="[%(name)s] [%(process)s] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s",
                 color=False, set_handlers_format="all"):
        self.logger = logging.getLogger(logger_name)
        self.custom_handler = logging.StreamHandler()
        self.logger.setLevel(logger_level)
        self.logger.addHandler(self.custom_handler)
        if set_handlers_format == "all":
            for logger_name in logging.root.manager.loggerDict:
                default_logger = logging.getLogger(logger_name)
                for handler in default_logger.handlers:
                    handler.setFormatter(CustomFormatter(format_handler, color))
        if type(set_handlers_format) is list:
            for logger_name in set_handlers_format:
                default_logger = logging.getLogger(logger_name)
                for handler in default_logger.handlers:
                    handler.setFormatter(CustomFormatter(format_handler, color))
        self.logger.info(
            f'Logger "{self.logger.name}" has been created. logger.level={self.logger.level}')


@lru_cache
def get_logger(logger_name: str = 'logger', logger_level=logging.DEBUG,
               format_handler: str = "[%(name)s] [%(process)s] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s",
               color: bool = False, set_handlers_format: str = "all"):
    return Logger(**locals()).logger
