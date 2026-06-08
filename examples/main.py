import logging
import time
import os

from model import ModelBroker
from client import Client
from importlib.metadata import version, PackageNotFoundError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ParseException(Exception):
    pass


def get_version():
    __version__ = "unknown"
    try:
        __version__ = version("ragebait")
    except PackageNotFoundError:
        logging.warning(
            "could not read pacakge version, ensure project is installed properly"
        )
    return __version__


def main():
    __version__ = get_version()
    logging.info(f"Running version {__version__}")

    delay_hours = os.environ.get("DELAY_HOURS", 12)
    ollama_client = Client()
    model_broker = ModelBroker(llm_client=ollama_client)
    delay_seconds = delay_hours * 60 * 60
    while True:
        model_broker.run()
        logging.info(f"next run in {delay_hours} hours...")
        time.sleep(float(delay_seconds))


if __name__ == "__main__":
    main()
