import logging


def configure_logging():
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
