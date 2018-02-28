import logging
import time

import docker

# Force UTC Timestamps
# From the logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

logformat = '%(asctime)s %(levelname)s:%(module)s:%(message)s'
dateformat = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='wumbotdocker.log', filemode='a', level=logging.INFO, 
                    format=logformat, datefmt=dateformat
                    )

client = docker.from_env()
APIClient = docker.APIClient()

# Find & kill any existing containers
dockername = 'wumbot-dev'
containerfilter = {'name':dockername}
wumbotcontainers = APIClient.containers(filters=containerfilter)
logging.info(f"Found {len(wumbotcontainers)} running {dockername} containers")
for container in wumbotcontainers:
    APIClient.stop(container['Id'])
else:
    logging.info(f"Killed {len(wumbotcontainers)} {dockername} containers")

# Build the new image
# docker build -t wumbot-dev .
logging.info(f"Building new {dockername} image...")
buildout = APIClient.build(path='.', tag=dockername)
logging.info([line for line in buildout])
logging.info(f"{dockername} image build complete")

# Restart the bot container
# docker run -d --rm --name wumbot-dev wumbot-dev
logging.info(f"Restarting {dockername}...")
client.containers.run(dockername, auto_remove=True, detach=True, name=dockername)
