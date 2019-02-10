import logging
import logging.config
import time
from pathlib import Path


LOGZIO_CONF_PATH = Path('./logzio.conf')

if LOGZIO_CONF_PATH.exists():
    logging.config.fileConfig('logzio.conf')
    logger = logging.getLogger('LogzioLogger')
else:
    # Default to local logging
    logging.Formatter.converter = time.gmtime  # Force UTC

    logformat = "%(asctime)s %(levelname)s:%(module)s:%(message)s"
    dateformat = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
        filename="./log/wumbot.log",
        filemode="a",
        level=logging.INFO,
        format=logformat,
        datefmt=dateformat,
    )
