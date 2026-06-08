# ragebait

create LLM driven reddit bots in python3

# installation

the project is only supported on linux and can only be built from source. Releases might become available later.

## building from source

grab the source code

```bash
git clone git@github.com:zeidlitz/ragebait.git
cd ragebait
```

setup a python3 virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

install packages and dependencies, see  `pyproject.toml` for full details

```bash
pip install .
```

run with a specified config.yaml

```bash
python3 main.py
```

# behaviour

define the model configuration in a `models.json` file, expected to reside in `assets/models/` relative to the root of the project, 

```json
[
  {
    "model_name": "goblin-lord",
    "username": "",
    "password": "",
    "client_id": "",
    "client_secret": "",
    "user_agent": "",
    "subreddits": [
      "stocks", "wallstreetbets", "askreddit", "RussianLiterature"
    ],
    "system_prompt": "You are a goblin. Respond to all user prompts as if you were a goblin. Your intressts are; horing gold, living under bridges, damp environments."
  },
]
```

when running the above model, it will take a random comment from one of the three configured subreddits, in this case it could be either, `/r/wallstreetbets`, `/r/askreddit` or `/r/RussianLiterature` and grab the latest comment made in them. The `system_prompt` will be fed to a llm completion endpoint with the comment as the `prompt`, the generated completion will be sent as a response to the comment.

# examples

Setting up a boilerplate model workloop using a ollama client with the default ollama configurations and a default small footprint model (llama-unsenscored:latest)

```python3
import time
from model import ModelBroker
from client import Client

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
```

To set a different llm client pass a configured client object to the `ModelBroker`:

```python3
llm_client = Client(host="myhost", port=123, protocol="https", model="deepseekv2")
model_broker = ModelBroker(llm_client=llm_client)
```

# requierments

a LLM serving completions on a `/completions` endpoint. Preferably any unsenscored model, or one that supports passing a system prompt. The core behaviour is meant to take a user defined system_prompt + another comment / post as prompt to generate the finalized completion output.
