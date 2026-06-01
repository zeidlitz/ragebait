import logging
import time
import os

from model import ModelBroker
from client import OllamaClient
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

    llm_model = os.environ.get("LLM_MODEL", "llama2-uncensored:latest")
    host = os.environ.get("LLM_HOST", "localhost")
    port = os.environ.get("LLM_PORT", "11434")
    protocol = os.environ.get("LLM_PROTOCOL", "http")
    delay_hours = os.environ.get("DELAY_HOURS", 12)
    ollama_client = OllamaClient(llm_model, host, port, protocol)
    model_broker = ModelBroker(ollama_client=ollama_client)
    delay_seconds = delay_hours * 60 * 60
    while True:
        model_broker.run()
        logging.info(f"next run in {delay_hours} hours...")
        time.sleep(float(delay_seconds))


if __name__ == "__main__":
    main()
