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
python3 main.py config.yaml
```


# requierments

a LLM serving completions on a `/completions` endpoint. Preferably ollama.

