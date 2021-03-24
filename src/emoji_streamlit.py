# pylint: skip-file
from pathlib import Path

import gensim.models as gsm
import numpy as np
import streamlit as st

ROOT_PATH = Path(__file__).parents[1].absolute()
MODEL_FOLDER = ROOT_PATH / "model"
text = [
    "🎉",
    "🎊",
    "📱",
    "📧",
    "💻",
    "⭐",
    "😉",
    "😍",
    "🎤",
    "💋",
    "👸",
    "🍑",
    "😭",
    "💘",
    "🍴",
    "🍻",
    "⛄",
    "🌎",
    "📍",
    "👀",
    "🏰",
    "🌈",
    "🎂",
    "🍳",
    "😋",
    "🍾",
    "🇰🇷",
]


@st.cache(allow_output_mutation=True)
def load_model():
    # Cache data and model loading
    e2v = gsm.KeyedVectors.load_word2vec_format(
        MODEL_FOLDER / "emoji2vec.bin", binary=True
    )
    jodel = gsm.KeyedVectors.load_word2vec_format(
        MODEL_FOLDER / "jeed1488.keyed_vecors.bin", binary=True
    )
    return e2v, jodel


def get_similarity(emoji: str, emb_model: str, method: str) -> list:

    if emb_model == "e2v":
        model = e2v
    elif emb_model == "jodel":
        model = jodel
    else:
        raise ValueError("Model must be one of 'e2v' or 'jodel'")

    try:

        if method == "positive":
            result = [model.most_similar(e) for e in emoji][0]

        elif method == "negative":
            result = [model.most_similar(negative=e) for e in emoji][0]
    except:
        result = f"{emoji} not in vocabulary"

    return result


if __name__ == "__main__":
    e2v, jodel = load_model()

    # Streamlit UI starts here
    st.sidebar.header("Select options:")
    method = st.sidebar.radio("Select similarity method", ["positive", "negative"], 0)

    st.sidebar.subheader("Click Me!")
    random = st.sidebar.button("Randomize emoji")

    st.sidebar.subheader("Emoji Library")
    st.sidebar.write("[emojipedia](https://emojipedia.org/)")

    st.title("Emoji Embeddings")
    emojis = st.text_area("Input emoji:", value="👋", height=10, max_chars=2)

    random_header = st.empty()
    random_placeholder = st.empty()
    st.subheader("Most similar emojis")

    if random:
        emojis = np.random.choice(text)
        random_header.subheader("Random emoji:")
        random_placeholder.write(emojis)

    similarity_e2v = get_similarity(emojis, emb_model="e2v", method=method)
    similarity_jodel = get_similarity(emojis, emb_model="jodel", method=method)

    title_container = st.beta_container()
    col1, col2 = st.beta_columns([1, 1])
    with title_container:
        with col1:
            st.write("emoji2vec")
            try:
                st.write([f"{x}: {round(y,3)}" for (x, y) in similarity_e2v])
            except:
                st.write(similarity_e2v)

        with col2:
            try:
                st.write("jodel")
                st.write([f"{x}: {round(y,3)}" for (x, y) in similarity_jodel])
            except:
                st.write(similarity_jodel)
