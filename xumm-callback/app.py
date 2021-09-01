import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("## EVENT")
    logger.info("%s", event)
