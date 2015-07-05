import logging

def set_logger(filename):
    logger = logging.getLogger()
    hdlr = logging.FileHandler(filename)
    fmt_str = '[%(levelname)s %(asctime)s @ %(process)d] - %(message)s'
    formatter = logging.Formatter(fmt_str)
    hdlr.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
