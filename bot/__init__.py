import json
import logging
import time

import sentry_sdk


with open("./credentials.JSON", "r") as f:
    _tmp = json.load(f)
    SENTRY_ENDPOINT = _tmp.get("SENTRY_ENDPOINT", None)

if SENTRY_ENDPOINT:
    sentry_sdk.init(SENTRY_ENDPOINT)
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
