import logging
import time


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
