import glob
import json
import yaml
from jsonschema import validate, ValidationError

import streamlit as st
from streamlit import session_state as session

MODELS_PATH = "assets/models/"

INITIAL_SESSION = {
    "username": "",
    "subreddits": [],
    "system_prompt": "",
}

def load_schema():
    schema_path = MODELS_PATH + "schema.json"
    with open(schema_path, "r") as f:
        return json.load(f)


def init_models():
    model_files = glob.glob(f"{MODELS_PATH}**/*.yaml", recursive=True)
    if not model_files:
        return []

    models = {}
    schema = load_schema()
    for file_path in model_files:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            try:
                file_name = f.name.removeprefix(MODELS_PATH)
                validate(instance=data, schema=schema)
                models[file_name] = data
            except ValidationError as e:
                print(f"invalid model file {file_path}: {e.message}")
    return models or []


def init_session():
    for key, value in INITIAL_SESSION.items():
        if key not in session:
            session[key] = value


def load_model(models, model_name="default.yaml"):
    print(f"loading {model_name}")
    try:
        model = models.get(model_name)
        for key, _ in session.items():
            session[key] = model.get(key)

        return model
    except KeyError as e:
        print(f"could not load model {model_name}: {e}")


def create_model():
    pass

def main():
    init_session()
    models = init_models()
    _ = load_model(models)
    render(models)


def render(models):
    with st.sidebar:
        st.markdown(f"models available `{len(models)}`")
        load_new_container = st.container(horizontal=True)
        st.divider()
        with load_new_container:
            load_model_button = st.button("load", type="primary")
            if load_model_button:
                pass
            new_model_button = st.button("new", type="primary")
            if new_model_button:
                pass
        st.markdown(f"name: `{session.username}`")
        st.image("assets/static/goblin.png", width=175)
        with st.chat_message(""):
            st.write("hey, I'm a goblin")
        st.chat_input(f"talk to {session.username}")
        st.divider()

    model_metadata_container = st.container(horizontal=True)
    st.divider()

    with model_metadata_container:
        with st.container():
            st.text_area("system prompt", f"{session.system_prompt}")
            edit_system_prompt_button = st.button("edit", key="system_prompt_edit")
            if edit_system_prompt_button:
                st.rerun()
        with st.container():
            st.caption("active in")
            for subreddit in session.subreddits:
                st.badge("/r/" + subreddit)
            edit_subreddit_button = st.button("edit", key="subreddit_edit")
            if edit_subreddit_button:
                st.rerun()

    model_stats_container = st.container(horizontal=True)

    with model_stats_container:
        st.metric(label="upvotes", value="78", delta="8")
        st.metric(label="downvotes", value="-789", delta="-97")
        from numpy.random import default_rng as rng
        changes = list(rng(4).standard_normal(20))
        data = [sum(changes[:i]) for i in range(20)]
        delta = round(data[-1], 2)
        st.metric("overview", "/r/stocks", delta, chart_data=data, chart_type="bar", border=True)


if __name__ == "__main__":
    main()
