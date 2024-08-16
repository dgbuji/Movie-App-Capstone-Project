import logging

logging.basicConfig(
    level=logging.DEBUG,
    # filename = 'log.txt',
    format = "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

def get_logger(name):
    return logging.getLogger(name)

logger = logging.getLogger(__name__)

logger.debug("This message will be recorded.")
logger.info("This message will be recorded.")
logger.warning("This message will be recorded.")
logger.error("This message will be recorded.")
logger.critical("This message will be recorded.")