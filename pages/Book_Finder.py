import streamlit as st
import requests

st.set_page_config(
    page_title="SizzlClub · Book Finder",
    page_icon="📚",
    layout="wide"
)

# -------------- STYLES --------------
st.markdown(
    """
    <style>
    .sizzl-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4D6D, #FF8E6E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sizzl-subtitle {
        font-size: 1rem;
        color: #f5f5f5cc;
        margin-bottom: 1rem;
    }
    .sizzl-pill {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
        border-radius: 999px;
        background-color: #2b2b2f;
        color: #ffdee7;
        font-size: 0.8rem;
        border: 1px solid #ff4d6d33;
    }
    .sizzl-card {
        padding: 0.9rem 1rem;
        border-radius: 0.8rem;
        background-color: #121218;
        border: 1px solid #ffffff10;
        margin-bottom: 0.8rem;
    }
    .sizzl-meta {
        color: #cfcfd9;
        font-size: 0.9rem;
    }
    .sizzl-badge-soft {
        display: inline-block;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        font-size: 0.75rem;
        background-color: #ff4d6d22;
        color: #ff9bb0;
        margin-left: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------- HEADER --------------
st.markdown('<div class="sizzl-title">📚 SizzlClub · Book Finder</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sizzl-subtitle">Search for romance & spicy reads, then save your finds to discuss later in the community.</div>',
    unsafe_allow_html=True
)

st.write("")


# -------------- SIDEBAR --------------
with st.sidebar:
    st.markdown("### 🔎 Search filters")
    query = st.text_input("Title / author / keyword", placeholder="e.g. 'enemy to lovers', 'Talia Hibbert'")
    max_results = st.slider("Max results", 5, 30, 10, step=5)

    st.markdown("**Optional vibe filter (just for fun):**")
    vibe = st.selectbox(
        "Spice / trope energy",
        [
            "Any",
            "🌶️ Cozy & low spice",
            "🌶🌶 Medium tension",
            "🌶🌶🌶 High drama & spice",
        ],
        index=0,
    )

    search_clicked = st.button("Search Open Library")

st.markdown("---")


# -------------- HELPER: MAP VIBE TO TEXT --------------
def vibe_hint_text(v):
    if v == "🌶️ Cozy & low spice":
        return "cozy small town OR low-angst romance OR fade-to-black"
    if v == "🌶🌶 Medium tension":
        return "romantic tension, banter, some on-page spice"
    if v == "🌶🌶🌶 High drama & spice":
        return "dark romance OR explicit spice OR very messy characters"
    return None


# -------------- MAIN SEARCH LOGIC --------------
if search_clicked:
    if not query.strip():
        st.warning("Type in a title, author, or trope to search.")
    else:
        col_left, col_right = st.columns([3, 1], gap="large")
        with col_left:
            with st.spinner("Looking through the stacks at Open Library..."):
                url = "https://openlibrary.org/search.json"
                params = {"q": query, "limit": max_results}
                try:
                    resp = requests.get(url, params=params, timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                    docs = data.get("docs", [])
                except Exception as e:
                    st.error(f"Something went wrong while searching: {e}")
                    docs = []

            if not docs:
                st.info("No results found. Try tweaking your keywords.")
            else:
                st.markdown(f"#### Results for **{query}**")
                if vibe != "Any":
                    hint = vibe_hint_text(vibe)
                    if hint:
                        st.caption(f"Vibe hint: looking for books that might feel like → *{hint}*")

                for doc in docs:
                    title = doc.get("title", "Unknown title")
                    authors = ", ".join(doc.get("author_name", [])[:3]) or "Unknown author"
                    year = doc.get("first_publish_year", "N/A")
                    key = doc.get("key", "")

                    subjects = doc.get("subject", [])
                    # Try to pull a few romance-y keywords
                    romantic_tags = [s for s in subjects if any(
                        kw in s.lower()
                        for kw in ["romance", "love", "relationship", "kiss", "erotic", "adult"]
                    )]

                    with st.container():
                        st.markdown('<div class="sizzl-card">', unsafe_allow_html=True)
                        st.markdown(f"**{title}**", unsafe_allow_html=True)
                        st.markdown(
                            f'<span class="sizzl-meta">{authors} · First published: {year}</span>',
                            unsafe_allow_html=True
                        )

                        tag_line = ""
                        if romantic_tags:
                            chips = ", ".join(romantic_tags[:5])
                            tag_line = f"**Subjects:** {chips}"
                        elif subjects:
                            chips = ", ".join(subjects[:5])
                            tag_line = f"**Subjects:** {chips}"
                        else:
                            tag_line = "_No subject tags available._"
                        st.write(tag_line)

                        # Soft "spice" guess (purely vibes from subjects)
                        spice_guess = ""
                        lower_subj = " ".join(subjects).lower()
                        if any(word in lower_subj for word in ["erotic", "sex", "adult", "explicit"]):
                            spice_guess = "🌶🌶🌶 Likely high spice"
                        elif any(word in lower_subj for word in ["romance", "love", "relationship"]):
                            spice_guess = "🌶🌶 Probably romantic"
                        elif subjects:
                            spice_guess = "🌶 Might be more general fiction"

                        if spice_guess:
                            st.markdown(
                                f'<span class="sizzl-badge-soft">{spice_guess}</span>',
                                unsafe_allow_html=True
                            )

                        st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("### Tips")
            st.write(
                "- Try searching by **trope**: 'fake dating', 'arranged marriage', 'mafia romance'.\n"
                "- Add author names you already love.\n"
                "- Use the vibe dropdown to guide your thinking (it doesn't filter the API yet, just your choices)."
            )

            st.markdown("### Next up on SizzlClub")
            st.write(
                "- Save favourites to your own rec lists\n"
                "- Click through to start a discussion thread in the Community page\n"
            )

else:
    st.info("Start by searching for a book, trope, or author using the controls in the sidebar.")
    st.write("Try something like **'enemies to lovers'**, **'college romance'**, or an author you adore.")
