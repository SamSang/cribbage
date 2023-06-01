import logging

log_file_path = "cribbage.log"

logger = logging.getLogger("cribbage")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

log_format = logging.Formatter("%(name)s - %(message)s")
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)

awarder = logging.getLogger("award")

# award_format = logging.Formatter("%(name)s | %(message)s | %(turn_number)s")
award_format = logging.Formatter("%(name)s | %(message)s | turn %(turn_number)s")

awarder_console_handler = logging.StreamHandler()
awarder_console_handler.setLevel(logging.INFO)
awarder_console_handler.setFormatter(award_format)
awarder.addHandler(awarder_console_handler)

awarder_file_handler = logging.FileHandler(log_file_path)
awarder_file_handler.setLevel(logging.INFO)
awarder_file_handler.setFormatter(award_format)
awarder.addHandler(awarder_file_handler)

awarder.setLevel(logging.INFO)


hand = logging.getLogger("hand")

hand_format = logging.Formatter(
    "%(name)s | %(message)s | turn %(turn_number)s | stack %(stack)s | total %(stack_total)s | cut %(the_cut)s | %(scores)s |"
)

hand_console_handler = logging.StreamHandler()
hand_console_handler.setLevel(logging.INFO)
hand_console_handler.setFormatter(hand_format)
hand.addHandler(hand_console_handler)

hand_file_handler = logging.FileHandler(log_file_path)
hand_file_handler.setLevel(logging.INFO)
hand_file_handler.setFormatter(hand_format)
hand.addHandler(hand_file_handler)

hand.setLevel(logging.INFO)
