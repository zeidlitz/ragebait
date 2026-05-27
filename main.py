import os
import sys
import logging
import praw
import yaml
from importlib.metadata import version, PackageNotFoundError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ParseException(Exception):
    pass


def get_version():
    __version__ = "unknown"
    try:
        __version__ = version("data-extraction")
    except PackageNotFoundError:
        logging.warning(
            "could not read pacakge version, ensure project is installed properly"
        )
    return __version__


def load_config(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def load_config_from_env():
    return {
        "extraction_limit": int(os.environ.get("EXTRACTION_LIMIT", 25)),
        "extraction_intervall": int(os.environ.get("EXTRACTION_INTERVALL", 5)),
        "client_id": os.environ.get("CLIENT_ID", ""),
        "client_secret": os.environ.get("CLIENT_SECRET", ""),
        "user_agent": os.environ.get("USER_AGENT", ""),
        "subreddit": os.environ.get("SUBREDDIT", ""),
        "redis": {
            "host": os.environ.get("REDIS_HOST", "localhost"),
            "port": int(os.environ.get("REDIS_PORT", 6379)),
            "maxlen": int(os.environ.get("REDIS_MAXLEN", 100000)),
        },
        "producer_stream": os.environ.get("PRODUCER_STREAM", "data_extraction"),
        "consumer_group": os.environ.get("CONSUMER_GROUP", "data_extraction"),
    }


def parse_args():
    args = sys.argv
    nrArgs = len(args)
    if nrArgs == 1:
        return None
    if nrArgs > 2:
        raise ParseException(
            f"too many input arguments, recieved {nrArgs} need exactlly one. Recieved: {args[1:]}"
        )
    return args[1]


def create_redis_consumer_group(
    redis_client, producer_stream, consumer_group, _id, mkstream
):
    try:
        logging.info(f"creating consumer group {consumer_group} for {producer_stream}")
        redis_client.xgroup_create(
            producer_stream, consumer_group, id=_id, mkstream=mkstream
        )
    except Exception as e:
        logging.info(f"Exception {e}")
        pass


def run(reddit_client, subreddit, system_prompt):
    sr = reddit_client.subreddit(subreddit)
    for comment in sr.comments(limit=1):
        # print(subreddit)
        # print(comment.submission.title)
        # print(comment.body)
        print(system_prompt + comment.submission.title, comment.body)
        # comment.reply("I agree with this guy!")

def configure():
    try:
        config_path = parse_args()
    except ParseException as e:
        print(e)
        os._exit(1)
    if config_path is None:
        logging.info(
            "No config file supplied, loading config from environment variables"
        )
        config = load_config_from_env()
    else:
        try:
            config = load_config(config_path)
        except FileNotFoundError as e:
            print(f"could not open config: {e} ")
            os._exit(1)
    client_id = config.get("client_id", "")
    client_secret = config.get("client_secret", "")
    user_agent = config.get("user_agent", "")
    user_agent = config.get("subreddit", "stocks")
    subreddit = config.get("subreddit", "")
    system_prompt = config.get("system_prompt", "")
    username = config.get("username")
    password = config.get("password")
    reddit_client = praw.Reddit(
        username=username,
        password=password,
        client_id=client_id,
        subreddit=subreddit,
        client_secret=client_secret,
        user_agent=user_agent,
        read_only=False,
    )
    return reddit_client, subreddit, system_prompt


def main():
    __version__ = get_version()
    logging.info(f"Running version {__version__}")
    reddit_client, subreddit, system_prompt = configure()
    run(reddit_client, subreddit, system_prompt)

if __name__ == "__main__":
    main()
