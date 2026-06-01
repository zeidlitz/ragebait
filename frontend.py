from model import ModelBroker
from client import OllamaClient
from typing import Any

import streamlit as st
from streamlit import session_state as session


def init_session(model_broker):
    if "initialized" in session:
        return
    st.session_state.initialized = True
    load_session(model_broker.model)


def load_session(model):
    for key, value in model.items():
        session[key] = value


def load_model(models, model_name) -> dict[Any, Any]:
    try:
        for model in models:
            if model.get("model_name") == model_name:
                return model
    except KeyError as e:
        print(f"could not load model {model_name}: {e}")
        return {}
    return {}


@st.cache_resource
def new_ollama_client(llm_model, host, port, protocol):
    return OllamaClient(llm_model, host, port, protocol)


def create_model():
    pass


def main():
    # TODO: move theese upstream
    llm_model = "llama2-uncensored:latest"
    host = "localhost"
    port = "11434"
    protocol = "http"
    ollama_client = new_ollama_client(llm_model, host, port, protocol)
    model_broker = ModelBroker(ollama_client=ollama_client)
    init_session(model_broker)
    render(model_broker.models)


def select_model(models, model_name):
    for model in models:
        if model.get("model_name") == model_name:
            load_session(model)


def new_model(
    model_name,
    username,
    password,
    client_id,
    client_secret,
    picture,
    user_agent,
    subreddits,
    system_prompt,
):
    # TODO: implement
    print(
        model_name,
        username,
        password,
        client_id,
        client_secret,
        picture,
        user_agent,
        subreddits,
        system_prompt,
    )
    st.rerun()


def render(models):
    with st.sidebar:
        st.markdown(f"models available `{len(models)}`")
        load_new_container = st.container(horizontal=True)
        st.divider()
        with load_new_container:
            load_model_popover = st.popover(
                "load", type="primary", key="load_model_trigger"
            )
            with load_model_popover:
                for model in models:
                    model_name = model.get("model_name")
                    st.button(
                        model_name,
                        key=f"model_button_{model_name}",
                        on_click=select_model,
                        args=(
                            models,
                            model_name,
                        ),
                    )
                    ## TODO: Fix this rerun
                    # t.rerun()

            new_model_popover = st.popover(
                "new", type="primary", key="new_model_trigger"
            )
            with new_model_popover:
                st.markdown("Create a new model")
                model_name = st.text_input("model_name")
                username = st.text_input("username")
                password = st.text_input("password", type="password")
                client_id = st.text_input("client_id")
                client_secret = st.text_input("client_secret", type="password")
                picture = st.file_uploader("picture")
                user_agent = st.text_input("user_agent")
                subreddits = st.text_input("subreddits")
                system_prompt = st.text_input("system_prompt")
                create_button = st.button("create")
                if create_button:
                    new_model(
                        model_name,
                        username,
                        password,
                        client_id,
                        client_secret,
                        picture,
                        user_agent,
                        subreddits,
                        system_prompt,
                    )

        st.markdown(f"name: `{session.username}`")
        st.image(f"assets/static/{session.picture}", width=175)
        with st.chat_message(""):
            st.write("...")
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
        with st.container():
            st.markdown("latest comments:")
            st.markdown(f"*only goblins understand*")


if __name__ == "__main__":
    main()
