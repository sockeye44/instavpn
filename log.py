import logging, StringIO, pastee, time, sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

string_io = StringIO.StringIO()

pastebin_handler = logging.StreamHandler(string_io)
pastebin_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
console_handler.setFormatter(formatter)
pastebin_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(pastebin_handler)


def log_debug(msg):
    logger.debug(msg)


def log_info(msg):
    logger.info(msg)


def log_warn(msg):
    logger.warn(msg)


def log_error(msg):
    logger.critical(msg)
    time.sleep(0.1)
    print('CRITICAL ERROR!')
    print('Crash report: ' + pastee.PasteClient().paste(string_io.getvalue()))
    print('Support: https://github.com/sockeye44/instavpn/issues')
    sys.exit(1)