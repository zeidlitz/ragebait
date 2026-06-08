import json
import random
import jsonschema
import logging
import praw

from client import Client, ClientException
from typing import Any
from prawcore.exceptions import OAuthException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ModelException(Exception):
    pass


class ModelBroker:
    def __init__(
        self,
        llm_client: Client,
        model_name: str = "",
    ):
        self.models_path = "assets/models/"
        self.ollama_client = llm_client
        self.model_name = model_name
        self.models = self.load_models()
        self.model = self.load_model(self.model_name)
        self.client_id = self.model.get("client_id")
        self.client_secret = self.model.get("client_secret")
        self.user_agent = self.model.get("user_agent")
        self.subreddits = self.model.get("subreddits", [])
        self.system_prompt = self.model.get("system_prompt")
        self.username = self.model.get("username")
        self.password = self.model.get("password")
        self.reddit_client = praw.Reddit(
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            read_only=False,
        )

    def load_schema(self) -> dict:
        schema_path = self.models_path + "schema.json"
        with open(schema_path, "r") as f:
            return json.load(f)

    def load_models(self) -> list:
        models_file = self.models_path + "models.json"
        schema = self.load_schema()
        with open(models_file, "r") as f:
            models = json.load(f)
            try:
                jsonschema.validate(instance=models, schema=schema)
                return models
            except jsonschema.ValidationError as e:
                raise ModelException(f"could not load model file {e}")

    def load_model(self, model_name="") -> dict[Any, Any]:
        if model_name == "":
            return self.models[0]
        try:
            for model in self.models:
                if model.get("model_name") == model_name:
                    return model
        except KeyError as e:
            raise ModelException(f"could not load model {model_name}: {e}")
        return {}

    def run(self):
        if len(self.subreddits) == 0:
            raise ModelException("could not find any subreddits")
        subreddit = random.choice(self.subreddits)
        sr = self.reddit_client.subreddit(subreddit)
        try:
            for comment in sr.comments(limit=1):
                completion = self.ollama_client.get_completion(
                    system_prompt=self.system_prompt, prompt=comment.body
                )
                if completion is not None:
                    comment.reply(completion)
        except (ClientException, OAuthException) as e:
            logging.error(f"could not get completion: {e}")
        logging.info("run completed successfully")
