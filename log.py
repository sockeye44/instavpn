import logging, StringIO, pastee, time, sys

class PasteBinLoggingHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        self.buff = StringIO.StringIO()
        logging.StreamHandler.__init__(self, self.buff)

    def emit(self, record):
        logging.StreamHandler.emit(self, record)

        # If we hit a critical error, we'll paste and quit
        if record.levelno == logging.CRITICAL:
            url = pastee.PasteClient().paste(self.buff.getvalue())
            print("CRITICAL ERROR!")
            print(" Crash report: {}".format(url))
            print(" Support: https://github.com/sockeye44/instavpn/issues")
            sys.exit(1)


def setup_logging():
    # Get root logger and attach some formatters to it
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    pastebin_handler = PasteBinLoggingHandler()
    pastebin_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
        datefmt='%H:%M:%S')

    console_handler.setFormatter(formatter)
    pastebin_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(pastebin_handler)

