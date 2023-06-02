import logging

default_level = logging.INFO

console_level = logging.INFO + 1


def get_logger(
    name: str, log_format: str, file_path: str = "cribbage.log"
) -> logging.Logger:
    """
    return a logger
    configured with defaults for this project

    Only log to stream when the console level gets set
    """
    logger = logging.getLogger(name)

    log_formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(log_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)

    return logger


hand_format = "%(name)s | %(message)s | turn %(turn_number)s | stack %(stack)s | total %(stack_total)s | cut %(the_cut)s | %(scores)s |"

hand = get_logger("hand", hand_format)


award_format = "%(name)s | %(message)s | turn %(turn_number)s"

awarder = get_logger("award", hand_format)


logger_format = "%(name)s | %(message)s"

logger = get_logger("cribbage", logger_format)


human = logging.getLogger("human")

log_formatter = logging.Formatter(logger_format)

console_handler = logging.StreamHandler()
console_handler.setLevel(console_level)
console_handler.setFormatter(log_formatter)

human.addHandler(console_handler)

human.setLevel(console_level)
