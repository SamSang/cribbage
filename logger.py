import logging

logger = logging.getLogger('cribbage')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('cribbage.log')
file_handler.setLevel(logging.DEBUG)

log_format = logging.Formatter('%(name)s - %(message)s')
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
